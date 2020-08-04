class Server
{
   //REALTIME API CALL

   static get_all_active_sessions(callback, gameID, require_player_id, sim_time=-1) //gameID eg 'CRYSTAL'
   {
   //returns object of form:
      // {[SessID0, SessID1, SessID2, ... sessIDn]}
      let method_string = SIMULATION_MODE ? "sim_all_active_sessions" : "get_all_active_sessions";
      var post_string = `method=${method_string}&gameID=${gameID}&require_player_id=${require_player_id}`
      if (SIMULATION_MODE) {
         post_string = `method=${method_string}&gameID=${gameID}&require_player_id=${require_player_id}&sim_time=${sim_time}`
      }
      console.log(`Making request for all active sessions: ${post_string}`)
      Server._execute_request(callback, post_string)
   }
   //returns {} if there are no active sessions.

   static get_active_sessions_by_loc(callback, gameID, state, city, sim_time=-1)
   {
   //   GameID - str ID of game eg 'CRYSTAL'
   //   state - str state name as returned by get_all_active_sessions(GameID)
   //   city - str city name as returned by get_all_active_sessions(GameID)
   //   returns an array of active sessions eg
   //   [SessID0, SessID1, SessID2]
      let method_string = SIMULATION_MODE ? "sim_active_sessions_by_loc" : "get_active_sessions_by_loc";
      var post_string = `method=${method_string}&gameID=${gameID}&state=${state}&city=${city}`
      if (SIMULATION_MODE) {
         post_string = `method=${method_string}&gameID=${gameID}&state=${state}&city=${city}&sim_time=${sim_time}`
      }
      console.log(`Making request for active sessions by location: ${post_string}`)
      Server._execute_request(callback, post_string)
   }

   // Note: The _by_sessID functions below are probably going to mostly be run
   // in a row, so if its more efficient to input and output whole lists, that
   // is fine too.
   static get_features_by_sessID(callback, sessID, gameID, sim_time=-1, features=null){
   //   returns the features of specific (callback, active) sessID.
   //   takes optional argument features which if not null, is an array of feature names
   //   specifying which features to return. this would be like:
   //   ['GameStart','Fail','GameEnd'].
   //   Returns list of features in JSON format
      if (sessID != -1) {
         let method_string = SIMULATION_MODE ? "sim_features_by_sessID" : "get_features_by_sessID";
         var post_string = `method=${method_string}&sessID=${sessID}&gameID=${gameID}&features=${features}`;
         if (SIMULATION_MODE) {
            post_string = `method=${method_string}&sessID=${sessID}&gameID=${gameID}&features=${features}&sim_time=${sim_time}`
         }
         console.log(`Making request for features by session: ${post_string}`);
         Server._execute_request(callback, post_string);
      }
      else {
         throw `RTServer was asked to find features on invalid session ID ${sessID}!`;
      }
   }

   static get_feature_names_by_game(callback, gameID){
   //   returns all feature names of that game (callback, any format is fine)
      var post_string = `method=get_feature_names_by_game&gameID=${gameID}`;
      console.log(`Making request for feature names by game: ${post_string}`);
      Server._execute_request(callback, post_string);
   }

   static get_predictions_by_sessID(callback, sessID, gameID, sim_time=-1, predictions=null){
   //   returns the predictions of specific (callback, active) sessID.
   //   takes optional argument predictions which if not null, is an array of prediction names
   //   specifying which predictions to return. this would be like:
   //   ['probability to finish lv3' etc.].
   //   Returns list of predictions in JSON format
      if (sessID != -1) {
         let method_string = SIMULATION_MODE ? "sim_predictions_by_sessID" : "get_predictions_by_sessID";
         var post_string = `method=${method_string}&sessID=${sessID}&gameID=${gameID}&predictions=${predictions}`
         if (SIMULATION_MODE) {
            post_string = `method=${method_string}&sessID=${sessID}&gameID=${gameID}&predictions=${predictions}&sim_time=${sim_time}`
         }
         console.log(`Making request for predictions by session: ${post_string}`)
         Server._execute_request(callback, post_string)
      }
      else {
         throw `RTServer was asked to find predictions on invalid session ID ${sessID}!`;
      }
   }

   static get_prediction_names_by_game(callback, gameID){
   //   returns all prediction names of that game (any format is fine)
      var post_string = `method=get_prediction_names_by_game&gameID=${gameID}`
      console.log(`Making request for prediction names by game: ${post_string}`)
      Server._execute_request(callback, post_string)
   }

   /**
    * Private function to do actual execution of a request. 
    * Creates a post request with given callback and parameter string.
    * @param {*} callback 
    * @param {*} post_string 
    */
   static _execute_request(callback, post_string)
   {
      var req = new XMLHttpRequest();
      req.onreadystatechange = function()
      {
         if (this.readyState == 4 && this.status == 200)
         {
            callback(this.responseText.toString());
         }
         else
         {
            // console.log(`Status for ${post_string} is ${this.statusText}`);
         }
      }
      // use this to set any desired custom path to the "realtime" cgi script.
      // req.open("POST", `${rt_config.protocol}://${rt_config.host}/${rt_config.path}`, true);
      req.open("POST", `/opengamedata/realtime.cgi`, true);
      req.setRequestHeader("Content-type", "application/x-www-form-urlencoded");
      req.send(post_string);
   }

/*
Example flow: {
  as of right now, the only game we are thinking of is lakeland, but theoretically the user could choose any game
  populate sidebars/map with data from realtime_api.get_all_active_sessions(gameID)
  user clicks on a state and a city
  optional: user can select subset of features/predictions to display from realtime_api.get_feature/prediction_names_by_game(gameID)
  Every ~5 seconds populate table with subset of features/predictions by {
    loop through sessID in realtime_api.get_active_sessions_by_loc(gameID, state, city)
    set i-th row of the table equal to cells derived from:
      realtime_api.get_predictions_by_sessID(sessID, predictions=subset)
  }



}
*/
}
