You are helping me configure my zeroclaw agent. This agent mostly helps with stock analysis. I'm bring you in (ie. the "big guns") to build out all the skills and scripts the agent will use. I need your help with setting up the systems the daily model will use. 

# Folders
The folder we start in is the zeroclaw `agents` folder with sub-folders for each agent. Currently there is just one agent called Barry who is performing all the analysis. Barry has a workspace folder with the following sub-folders are where we will be doing most of our work:
* skills - the skills used by the agent for stock analysis and related tasks
* investment - results produced by the agent includes stock and market reports

No touching the agent's memories pls, unless explcitly asked.

# Documentation style
Treat any documentation you write or modify as technical documentation. Be concise and clear. Carefully consider both what to include and what to leave out. We want high information density and minimal repetition. 

Just like in code, we want a single source of truth in our docs. Each concept/description/explanation should exist in a single place in docs. If a single concept/description/explanation is relevant across multiple sections/pages in the docs, then provide the minimal possible re-hash and link to the source-of-truth for a more detailed explanation. We don't want the same thing explained multiple times across multiple pages.

When updating existing documentation, do not refer back how things used to be or explain why it changed. Someone reading the documentation for the first time should be able to understand it without prior knowledge of earlier revisions, and without being burdened with unneccessary information about what has changed over time. We can use git history to track how the documentation has evolved if needed.

# Coding Style
Sometimes we will make changes to scripts which breaks backwards-compatibility with data sources. Do not aim to make scripts backwards compatible with old data formats unless specifically asked to. The default should be to keep the scripts cleanly focussed on the current data format, and migrate all existing data into the new format.

# General Approach
* Make small changes at a time. Start simple, and build up complexity as we go. 

# AGENTS.md
`AGENTS.md` from agent sub-folders is intended for the daily model - not you. If it is fed to you on start-up please ignore it.


Let's go!