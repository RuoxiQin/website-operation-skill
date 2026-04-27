import { readFileSync } from 'node:fs';
import { fileURLToPath } from 'node:url';
import { dirname, join, resolve } from 'node:path';
import {
  AuthStorage,
  DefaultResourceLoader,
  ModelRegistry,
  SessionManager,
  SettingsManager,
  createAgentSession,
  getAgentDir,
} from '@mariozechner/pi-coding-agent';
import { getModel } from '@mariozechner/pi-ai';

const here = dirname(fileURLToPath(import.meta.url));
const cwd = here;

const promptsPath = resolve(here, '../prompts/sample-tasks.json');
const prompts = JSON.parse(readFileSync(promptsPath, 'utf8'));
const requestedName = process.argv[2];
const selected = requestedName
  ? prompts.find(p => p.name === requestedName)
  : prompts[0];
if (!selected) {
  const available = prompts.map(p => p.name).join(', ');
  throw new Error(`Prompt "${requestedName}" not found in ${promptsPath}. Available: ${available}`);
}
const prompt = selected.prompt;

const modelId = process.env.MODEL ?? 'gemini-2.5-pro';
const model = getModel('google', modelId);
if (!model) throw new Error(`Unknown model: google/${modelId}`);

const agentDir = getAgentDir();
const authStorage = AuthStorage.create(join(agentDir, 'auth.json'));
const modelRegistry = ModelRegistry.create(authStorage, join(agentDir, 'models.json'));

const settingsManager = SettingsManager.create(cwd, agentDir);
// noSkills: true blocks BOTH project-local (.pi/skills/) and global (~/.pi/agent/skills/)
// discovery, so the comparison is clean even if the user has personal skills installed.
// noContextFiles is intentionally NOT set — both agents should still load examples/AGENTS.md
// (environment facts that aren't part of the with-skill vs without-skill variable).
const resourceLoader = new DefaultResourceLoader({
  cwd,
  agentDir,
  settingsManager,
  noSkills: true,
  noExtensions: true,
  noPromptTemplates: true,
  noThemes: true,
});
await resourceLoader.reload();

const loadedSkills = resourceLoader.getSkills().skills;
const loadedContext = resourceLoader.getAgentsFiles().agentsFiles;
console.error(`[pi-without-skill] loaded skills:        ${loadedSkills.map(s => s.name).join(', ') || '(none)'}`);
console.error(`[pi-without-skill] loaded context files: ${loadedContext.map(f => f.path).join(', ') || '(none)'}`);
console.error(`[pi-without-skill] model:                google/${modelId}`);
console.error(`[pi-without-skill] prompt:               ${promptsPath} (${selected.name})`);
console.error('---');

const { session } = await createAgentSession({
  cwd,
  agentDir,
  authStorage,
  modelRegistry,
  model,
  resourceLoader,
  sessionManager: SessionManager.inMemory(),
  settingsManager,
});

await new Promise((resolveDone, rejectDone) => {
  session.subscribe(event => {
    if (event.type === 'message_update' && event.assistantMessageEvent.type === 'text_delta') {
      process.stdout.write(event.assistantMessageEvent.delta);
    } else if (event.type === 'tool_execution_start') {
      process.stderr.write(`\n[tool] ${event.toolName} ${JSON.stringify(event.args).slice(0, 200)}\n`);
    } else if (event.type === 'agent_end') {
      process.stdout.write('\n');
      resolveDone();
    }
  });
  session.prompt(prompt).catch(rejectDone);
});

session.dispose();
