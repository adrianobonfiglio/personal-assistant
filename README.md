# Introduction
Project consist in a Alexa style personal assistant that recognize user's speech transform to text, using pre-defined actions like play music or open personal stuff. Also, it uses agentic AI with langchain to decide on what tools to use for specifc actions. The agent is powered by Google Gemini.
The assistant is built to be installed in a raspberry pi 5 connected to a touch screen monitor to listen to user and show the actions.

# Issues
## Mac issue with pyaudio and SpeechRecoginition
When executing on Mac M1, M2... there an issue when executing speech Recognition and pyaudio as this libraries compile to run in Intel based CPU.
To fix the issue, execute the following command:
```console
softwareupdate --install-rosetta
```