## 1. Exercise Source
See `docs/exercises/09-integrate-agent-into-joule.md` for the normative procedure.
## 2. Verify Cloud Foundry Deployment From Exercise 08
Confirm the A2A server from Exercise 08 is running before starting Joule work.
Assume working directory is `starter-project` unless stated otherwise.
### Automated Checks
Obtain the app route from Cloud Foundry in a code block below.
```bash
cf apps
```
Expected route is `investigator-graph-mikisven.cfapps.eu10-004.hana.ondemand.com`.
Run the health check in a code block below.
```bash
curl https://investigator-graph-mikisven.cfapps.eu10-004.hana.ondemand.com/health
```
Run the agent-card check in a code block below.
```bash
curl https://investigator-graph-mikisven.cfapps.eu10-004.hana.ondemand.com/.well-known/agent-card.json
```
Proceed only if health returns ok and the agent card shows the investigate skill.
Expected health body is `{"status": "ok"}`.
## 3. Align Server State With Graph State
`server.py` now includes `"intelligence_report": None` in local code.
### Required Redeploy Check
Redeploy from `starter-project` because local code is newer than the running app.
```bash
cf push "investigator-graph-mikisven"
```
Re-run Section 2 checks after redeployment.
## 4. Human: Check Node.js Runtime
Open a terminal in BAS or locally.
### Required Human Action
Run the version check in a code block below.
```bash
node -v
```
Install Node.js v20.12.0 through v24 if the version is missing or incompatible.
## 5. Install Joule Studio CLI
Install the CLI globally after Node.js is ready.
### Installation Commands
Run the install command in a code block below.
```bash
npm install -g @sap/joule-studio-cli
```
Run the verification command in a code block below.
```bash
joule -V
```
## 6. Human: Log In To Joule
Obtain IAS authentication URL, Joule API URL, client ID, client secret, username, and password from the instructor.
### Required Human Authentication
Run the login command in a code block below.
```bash
joule login
```
Enter all prompted values interactively without storing secrets in the repository.
Run the status command in a code block below.
```bash
joule status
```
Repeat `joule login` if later commands report an authentication error.
## 7. Human: Create BTP Destination In Browser
Open the BTP subaccount cockpit in a browser.
Navigate to Connectivity and then to Destinations.
### Required Destination Values
Create a destination named `INVESTIGATOR_AGENT_MIKISVEN`.
Set type to HTTP.
Set URL to `https://investigator-graph-mikisven.cfapps.eu10-004.hana.ondemand.com` without a trailing path.
Set proxy type to Internet.
Set authentication to NoAuthentication.
Save the destination before continuing.
Use exactly the same destination name in Section 9.
## 8. Create Joule Directory Structure
Create the local capability folders from `starter-project`.
### Creation Commands
Run the directory commands in a code block below.
```bash
mkdir -p joule/investigator_capability/functions
mkdir -p joule/investigator_capability/scenarios
```
## 9. Create Capability Descriptor
Create `joule/investigator_capability/capability.sapdas.yaml` relative to `starter-project`.
Use `schema_version: 3.28.0`.
Use `namespace: joule.ext`.
Use capability name `investigator_capability`.
Map system alias `INVESTIGATOR_AGENT` to destination `INVESTIGATOR_AGENT_MIKISVEN`.
## 10. Create Investigate Scenario
Create `joule/investigator_capability/scenarios/investigate_scenario.yaml` relative to `starter-project`.
Describe art-theft investigation with appraisal, evidence, suspects, and report keywords.
Point scenario target to function `investigate_function`.
## 11. Create Investigate Function
Create `joule/investigator_capability/functions/investigate_function.yaml` relative to `starter-project`.
Add an `agent-request` action with system alias `INVESTIGATOR_AGENT`.
Use `agent_type: remote` for the Cloud Foundry code-based agent.
Store the response in `apiResponse`.
Add a markdown `message` action reading `apiResponse.body.artifacts[0].parts[0].text`.
## 12. Create Digital Assistant Descriptor
Create `joule/da.sapdas.yaml` relative to `starter-project`.
Use Digital Assistant schema `1.4.0`.
Name the assistant `investigator_assistant`.
Include local capability folder `./investigator_capability`.
## 13. Compile And Deploy Capability
Change into `joule` from `starter-project` before deploying.
```bash
cd joule
```
### Deployment Commands
Run the deploy command in a code block below.
```bash
joule deploy -c -n "investigator_assistant_mikisven"
```
Expect only the optional low-severity i18n warning about a missing folder.
Run the listing command in a code block below.
```bash
joule list
```
Confirm `investigator_assistant_mikisven` appears in the deployed assistants.
## 14. Human: Test Capability In Joule Chat
Launch the test client from the terminal.
### Required Human Test
Run the launch command in a code block below.
```bash
joule launch "investigator_assistant_mikisven"
```
Send the art-theft investigation request for Sophie Dubois, Marcus Chen, and Viktor Petrov in Joule chat.
Allow up to two minutes because RPT-1, grounding, and web search run sequentially.
Confirm that Joule displays the markdown investigation report.
## 15. Human: Verify End-To-End Result And Handle Failures
Check destination `INVESTIGATOR_AGENT_MIKISVEN`, system alias, agent card, and health endpoint on mismatch.
### Failure Commands
Inspect recent Cloud Foundry logs in a code block below.
```bash
cf logs investigator-graph-mikisven --recent
```
Reduce grounding `maxChunkCount` or simplify the request if Joule reports a 60-second timeout.
