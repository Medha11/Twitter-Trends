# Plan

* First extractor extracts tweets as usual.
* Tweets are cleaned and dumped into MongoDB.
* Aggregation is done for the whole day.
* Based on the aggregation, top 100 entities are found and the respective tweets are clubbed into one collection.
* Before it is dumped into the collection, sentiment analysis is done on them.
* Using each of the 100 collections as a separate document, LDA is performed. If 100 documents is too low, we can split the big documents into smaller ones.
* The tweets are iterated individually to find the topic to which it belongs.
* URLs are extracted for each topic which seem to be most relevant.
* Webpages corresponding to the URLs are downloaded and parsed.
* A portion of the main content can be displayed after extraction.
* The graph is approximated as usual but the time span has to be discussed upon.
* The graph, related tweets and summarizations of the URLs along with the hyperlinks is displayed for each topic on the portal.

# Workflow

* Control of engine starts with **manager.py**
* **manager.py** makes us of *multiprocess* and *subprocess* to spawn extractor, preprocessor and postprocessor as separate processes
* **config.py** in the **utilities** package stores tuning parameters such as 'alarm' times, file limit etc.
* Refer to [this](https://drive.google.com/open?id=0B4cI0VUerUweWU1hT3htenhmUzA) .ppt for further information.

# Dataset

* Download dataset(s) from the [Drive folder](https://drive.google.com/folderview?id=0B4cI0VUerUweVWhuOGJSTGR0b28&usp=sharing "Google Drive")
  * The **full_dataset.rar** contains all **2 Million** tweets
  * Optionally, you can download parts of this dataset from the **Parts** folder, each _(dataset\*.rar)_ containing **200,000** tweets 
  * Each *.json* file contains **10,000** tweets
  
# init

* **Clone** the git repository
* Run **python_path.bat** to add **PYTHONPATH** env variable. This needs to be done only **once**
* Make necessary changes in the **config.py** file in **engine\utilities\**
* Run **python init.py** in Command Prompt to start engine
* To stop, close **all** Command Prompt and Python windows

# Portal

* The **portal** folder is the django project for the web portal
* Create a database called 'trends'
* In the settings file, change password for mysql root, in case it is different
* Run createsuperuser to create an admin
* Create some top trends using the admin site. I have included a screenshot for UI after creating some sample topics(with ranks). It will redirect to the details page after clicking(see screenshots).
* Homepage can be opened using the url: 127.0.0.1:8000 or localhost:8000
* TopTrends model has a topic object and a rank object. Will be modified to include graphs n all when implementation is done.

