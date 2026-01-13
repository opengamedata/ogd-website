import re
from datetime import date, timedelta
from typing import Dict, Optional

from flask import Flask, render_template, current_app, request

from config.AppConfig import AppConfig
from includes import services
from models.GameCard import GameCard
from models.GameDetails import GameDetails
from models.GameFileInfo import GameFileInfo
from models.PipelineElement import PipelineElement

app = Flask(__name__, static_folder="assets")
app.config.update(AppConfig.APP_CONFIG)

@app.template_filter('log')
def log(msg:str, level:str="INFO"):
    match level.upper():
        case "ERR" | "ERROR":
            app.logger.error(msg)
        case "WARN" | "WARNING":
            app.logger.warning(msg)
        case "INFO" | "INFORMATION":
            app.logger.info(msg)
        case "DEBUG":
            app.logger.debug(msg)
    return ''

@app.route("/")
@app.route("/index")
@app.route("/index.html")
def index():
    # Get game list
    gamelist = services.getGameList()
    games = []
    for game_id,game_details in gamelist.items():
    # foreach(gamelist as key => value)
        # Get game usage from api for each game
        game_usage = services.getGameUsage(game_id=game_id)
        game_card = GameCard(GameDetails.FromDict(game_id=game_id, data=game_details), game_usage)
        games.append(game_card)

    return render_template("index/index.html", games=games, display_version=AppConfig.APP_CONFIG.get("DISPLAY_VERSION", True))
    
@app.route("/about")
@app.route("/about.html")
def about():
    return render_template("about/about.html", display_version=AppConfig.APP_CONFIG.get("DISPLAY_VERSION", True))

@app.route("/getinvolved")
@app.route("/getinvolved.html")
def getinvolved():
    return render_template("getinvolved/getinvolved.html", display_version=AppConfig.APP_CONFIG.get("DISPLAY_VERSION", True))

@app.route("/gamedata")
@app.route("/gamedata.html")
def gamedata():
    """ Generate the gamedata page.

    From old comment block, might be useful for figuring out what we previously identified as things to improve about the generation of the page:

    > This file is a bit complicated, as the page itself had/has a *lot* of object parsing, date manipulation, and other business logic in what ought to be the "view" portion of the code.
    > While this has been cleaned up somewhat, there remains a lot going on in the page construction.
    > To create a reasonable tradeoff between coupling and cohesion, the file is structured as follows:
    > 1. Declaration: A <?php?> tag containing imports, calls to services functions, and construction of a few elements that are used in multiple sections.
    > 2. Section Generation: A <?php?> tag containing function definitions to render each <section> of the page.
    >     These functions have a structure that mirrors the overall file structure:
    >     * Declaration: declaring of local variables, including defaults for elements of the <section>.
    >     * Element Generation: A check for null inputs, wrapped around logic to generate the "intended" elements of the <section>
    >         The defaults set in the "Declaration" section typically include a message saying the element could not be generated due to null data.
    >         Thus, if the check for null inputs fails, there will be a reasonable explanation rather than a crash.
    >     * Section Construction: A return statement that assembles the elements within the structure of the <section>.
    > 3. Page Construction: A <?php?> tag that assembles the sections together into the structure of the page.
 
    > Keeping this structure in mind, it should be easier to navigate the file and update logic.
    > In the future, some of the business logic embedded into the section generation functions could be factored out into proper control classes,
    > and then it might be possible to push this file closer to a typical HTML-oriented PHP page script.

    :return: _description_
    :rtype: _type_
    """

    # Declare variables
    game_details = None
    game_files = None
    buttons = None

    raw_game_id = request.args.get("game")
    if raw_game_id is not None and raw_game_id != '':
        # 1. sanitize game ID by removing any characters that aren't alpha-numeric or an underscore
        game_id : str = re.sub("/[^a-zA-Z0-9-_]+/", "", raw_game_id).upper()
        # 2. Get game details from the game_list file.
        game_details = services.getGameDetails(game_id)
        if not game_details:
            err_str = f"Failed to find game details for game_id={game_id}, got no response object!"
            current_app.logger.error(err_str)
        # 3. Get game file info from API
        # In order to provide a meaningful param for year and month, do what the API originally did and just set last month as our starting selection.
        last_month = date.today().replace(day=1) - timedelta(days=1)
        game_files = services.getGameFileInfoByMonth(game_id, year=last_month.year, month=last_month.month)
        if not game_files:
            err_str = f"getGameFileInfoByMonth request, for game_id={game_id} with year=null and month=null, got no response object!"
            current_app.logger.error(err_str)
        buttons = generatePipelineButtons(game_files)
    else:
        err_str = "gamedata.html got request with no game parameter!"
        current_app.logger.error(err_str)
    return render_template("gamedata/gamedata.html", game_details=game_details, game_files=game_files, buttons=buttons, display_version=AppConfig.APP_CONFIG.get("DISPLAY_VERSION"))

def generatePipelineButtons(game_files:Optional[GameFileInfo]) -> Dict[str, PipelineElement]:
    raw_files        = {}
    detectors_files  = {}
    event_files      = {}
    extractors_files = {}
    feature_files    = {}
    month_name = "NO MONTH AVAILABLE"

    if game_files:
        raw_files        = { 'Raw Data':game_files.RawFileLink }             if game_files.RawFileLink    else {}
        detectors_files  = { 'Detectors':game_files.DetectorsLink }          if game_files.DetectorsLink  else {}
        event_files      = { 'Calculated Events':game_files.EventsFileLink } if game_files.EventsFileLink else {}
        extractors_files = { 'Extractors':game_files.FeaturesLink }          if game_files.FeaturesLink   else {} # aka Extractors or Feature Extractors
        feature_files    = game_files.FeatureFiles                           if game_files.FeatureFiles   else {}
        month_name       = game_files.LastDate.strftime("%B")                if game_files.LastDate       else month_name


    # Create Pipeline buttons (including the transition buttons)
    # title, image, image_active, selector, file_links, month, text, is_active, is_a_transition_button)
    raw_description      = 'Time-sequenced data as provided by the game directly. Includes player events, system feedback and game progression.'
    events_description   = 'Raw time-sequenced data interwoven with with events generated by automated detectors.'
    features_description = 'Feature-engineered data that describe game-play at different levels of aggregation.'
    return {
        "raw" :  PipelineElement(
            title='Raw Data',             text=raw_description,
            month=month_name,             file_links=raw_files,
            image='pipeline-raw.svg',     image_active='pipeline-raw-active.svg',
            selector='raw',               is_transition_button=False,
            is_active=len(raw_files) > 0
        ),
        "detectors" :  PipelineElement(
            title='Detectors',                  text='',
            month=month_name,                   file_links=detectors_files,
            image='pipeline-transform-btn.png', image_active='pipeline-transform-active.svg',
            selector='detector',                is_transition_button=True,
            is_active=len(raw_files) == 0 and len(detectors_files) > 0
        ),
        "events" :  PipelineElement(
            title='Calculated Events',  text=events_description,
            month=month_name,           file_links=event_files,
            image='pipeline-event.svg', image_active='pipeline-event-active.svg',
            selector='event',           is_transition_button=False,
            is_active=len(raw_files) == 0 and len(detectors_files) == 0 and len(event_files) > 0
        ),
        "extractors" :  PipelineElement(
            title='Extractors',                 text='',
            month=month_name,                   file_links=extractors_files,
            image='pipeline-transform-btn.png', image_active='pipeline-transform-active.svg',
            selector='extractor',               is_transition_button=True,
            is_active=len(raw_files) == 0 and len(detectors_files) == 0 and len(event_files) == 0 and len(extractors_files) > 0
        ),
        "features" :  PipelineElement(
            title='Feature Data',         text=features_description,
            month=month_name,             file_links=feature_files,
            image='pipeline-feature.svg', image_active='pipeline-feature-active.svg',
            selector='feature',           is_transition_button=False,
            is_active=(len(raw_files) == 0 and len(event_files) == 0 and len(extractors_files) == 0 and len(feature_files) > 0),
        )
    }

if __name__ == '__main__':
    app.run()