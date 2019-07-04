## Sums of 4

- start event_name = athena.games.sums.start
- stop event_name = athena.games.sums.stop

- Game state = SUMS

## GUI
- Inside `gui` folder. Two files, `tkNotebook.py` and `wizardOfOzRemote.py`
- Currently two Tabs (created at their respective functions): SumsTab for the sums-of-numbers-game and EmorecTab for the emotion-expression game
- To add a new Tab follow the same structure as the two functions
- There is the possibility to add Labels (with the `Label` class) and Buttons (with the `self.add_button` method)
- To run, execute in the terminal: `python wizardOfOzRemote.py`

## How to run
1) Copy the dialogue from dialogue/Data_CollectionFlow.xml to the respective IrisTK project folder
2) Compile the flow with the IrisTK compile tool
3) Open an IrisTK broker (`iristk broker`)
4) Set the broker address in the `config.py` file at the `broker` entry
5) Open the GUI by running `python wizardOfOzRemote.py` inside the `gui` folder
6) Run `python run_all_games.py`
7) Run the IrisTK flow from Eclipse
8) Open the `zeno/zeno_mvn` Maven project in NetBeans, build it and run it
