<?php

require_once 'config/AppConfig.php';
require_once 'includes/services.php';
require_once 'models/APIResponse.php';
require_once 'models/GameDetails.php';
require_once 'models/GameUsage.php';
require_once 'models/GameCard.php';
require_once 'components/Card.php';

// Get game list
$gamelist = services\getGameList();
$games = [];
foreach($gamelist as $key => $value)
{
    // Get game usage from api for each game
    $game_usage = null; // services\getGameUsage($key);

    $game_card = new GameCard(GameDetails::fromArray($key, $value), $game_usage);
    array_push($games, $game_card);
}

?>
<?php require 'includes/header.php'; ?>
<section class="hero w-100 px-3 py-5 px-md-5 bg-dark text-white d-flex">
    <div class="col-sm-6 mt-auto my-md-auto">
        <h1 class="display-1">Welcome to Open Game Data</h1>
        <p class="lead">We are leveraging data science to create meaningful insights out of mountains of player data.</p>
        <div class="text-nowrap">
            <a href="#gamelist" class="btn btn-primary me-3">View Games</a> 
            <a href="https://opengamedata.io" target="_blank" class="btn btn-dark">Learn More</a>
        </div>
    </div>
</section>

<p> Open Game Data is an open-source and community-maintained infrastructure for conducting ethical research with educational game data. From the logging libraries that developers can integrate into learning games, all the way to the analytics that allow researchers to test new theories, we prioritize privacy, modularity, scalability, and performance.</p>

       <div class="d-flex flex-wrap flex-sm-nowrap mb-5">
            <div class="img-col mx-auto my-auto">
                <img class="img-fluid" src="assets/images/icons/add-game.svg" alt="">
            </div>
            <div class="flex-fill mt-4">
                <h2>Add your game to OGD</h2>
                <p>Want to start logging to OGD? <a href = "https://github.com/opengamedata/opengamedata-website/issues/new?template=02-submit-new-game.yml">Submit your Game </a>(Github Account Required)</p>
            </div>
        </div>
        <div class="d-flex flex-wrap flex-sm-nowrap mb-5">
            <div class="img-col mx-auto my-auto">
                <img class="img-fluid" src="assets/images/icons/cite-ogd.svg" alt="">
            </div>
            <div class="flex-fill mt-4">
                <h2>Cite OGD in your projects</h2>
                <p>
                    Gagnon, D., Swanson, L. (2023). Open Game Data: A Technical Infrastructure for Open Science with Educational Games. In: Haahr, M., Rojas-Salazar, A., Göbel, S. (eds) Serious Games. JCSG 2023. Lecture Notes in Computer Science, vol 14309. Springer, Cham. <a href ="https://doi.org/10.1007/978-3-031-44751-8_1">https://doi.org/10.1007/978-3-031-44751-8_1</a>
                </p>
            </div>
        </div>
        <div class="d-flex flex-wrap flex-sm-nowrap mb-5">
            <div class="img-col mx-auto my-auto">
                <img class="img-fluid" src="assets/images/logos/creative-commons.svg" alt="">
            </div>
            <div class="flex-fill mt-4">
                <h2>Copyright license and Usage</h2>
                <p><a href="https://creativecommons.org/publicdomain/zero/1.0/" target="_blank">https://creativecommons.org/publicdomain/zero/1.0/</a></p>
            </div>
        </div>



<main id="dashboard">
    <section id="gamelist" class="container-fluid mb-5">
        <h2 class="mb-5 text-center">Featured Data Sets</h2>
        <div class="row row-cols-1 row-cols-sm-2 row-cols-md-3 row-cols-lg-4 g-4">
            <?php 
                foreach($games as $game_card) {
                    $card = new Card($game_card->getGame(),$game_card->getGameUsage());
                    echo $card->render();
                }
            ?>
        </div>
    </section>
</main>
<!-- Begin Footer Include -->
<?php require 'includes/footer.php'; ?>
