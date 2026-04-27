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

const promptPath = process.argv[2]
  ? resolve(process.cwd(), process.argv[2])
  : resolve(here, '../prompts/sample-task.txt');
const prompt = readFileSync(promptPath, 'utf8').trim();

const modelId = process.env.MODEL ?? 'gemini-2.5-pro';
const model = getModel('google', modelId);
if (!model) throw new Error(`Unknown model: google/${modelId}`);

const agentDir = getAgentDir();
const authStorage = AuthStorage.create(join(agentDir, 'auth.json'));
const modelRegistry = ModelRegistry.create(authStorage, join(agentDir, 'models.json'));

const settingsManager = SettingsManager.create(cwd, agentDir);
const resourceLoader = new DefaultResourceLoader({
  cwd,
  agentDir,
  settingsManager,
  noExtensions: true,
  noPromptTemplates: true,
  noThemes: true,
  noContextFiles: true,
});
await resourceLoader.reload();

const loadedSkills = resourceLoader.getSkills().skills;
console.error(`[pi-with-skill] loaded skills: ${loadedSkills.map(s => s.name).join(', ') || '(none)'}`);
console.error(`[pi-with-skill] model: google/${modelId}`);
console.error(`[pi-with-skill] prompt: ${promptPath}`);
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
