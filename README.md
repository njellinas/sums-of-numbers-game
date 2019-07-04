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
1) Copy the dialogue from dialogue/Data_CollectionFlow.xml
2) open a iristk broker
3) go to gui, and run python wizardOfOzRemote.py
4) run python run_all_games.py
5) compile and run the eclipse java script
6) build and run the zeno maven project
