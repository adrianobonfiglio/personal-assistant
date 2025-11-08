# Issues
## Mac issue with pyaudio and SpeechRecoginition
When executing on Mac M1, M2... there an issue when executing speech Recognition and pyaudio as this libraries compile to run in Intel based CPU.
To fix the issue, execute the following command:
```console
softwareupdate --install-rosetta
```