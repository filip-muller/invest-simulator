# Investing Simulator
 This is a library for simulating investing on historic or fictionary data
 
 ## Getting started
 First, clone the repository. Then find the file invest_simulator.py and copy it to you working folder.
 Then, in your python code type `from invest_simulator import InvestSimulator` to import the key class.
 
 ### Generating data
 Now, you're gonna need to generate data for the simulator to work with. The main method to do this
 is to generate them from a csv file using the method `InvestSimulator.vytvor_data_csv()`. This method takes
 the path to your csv file as the first argument (e.g. `"data.csv"`). The next argument specifies the format of
 the date being used in your csv file. It uses the same codes as the [datetime module](https://docs.python.org/3/library/datetime.html#strftime-and-strptime-format-codes). The next two arguments specify, which column of the csv includes the date and which includes the price.
 The columns are counted from 0.
 
 ### Creating the simulator
 Once you have generated the data, you can create a new simulator. Create a new instance of the class
 InvestSimulator and pass it the created data as the first argument. The second argument specifies, how much
 money should get added to the simulators balance every year (yearly income). The constructor takes many
 optional arguments, feel free to play around with them.
 
 ### Simulating
 The simulator has two main methods - `dalsi_den()`, which moves the simulation one day forward
 and `nakup()`, which buys stocks for the current market price in the simulation. You can specify the
 amount of cash to be used for the purchase, but by default the simulator will use all the cash.
 
 ### `pridej_automaticky_nakup(mesic, den=1)`
 Prida datum, kdy se kazdy rok automaticky nakoupi za veskerou hotovost.
 
