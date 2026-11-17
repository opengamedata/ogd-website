# opengamedata-website

Website front-end to the OpenGameData archive.

## Building and Running for Local Debugging

### Dev Requirements

- Node - newer version; setup with LTS 18.14.1
- cURL
- Python 3.12 or higher
  - Flask 2.3.3
  - See `requirements.txt` for more details

NOTE: a local install of PHP and the php_curl bindings are sufficient to test the site, though a full local Apache Server will provide the best emulation of the deploy environment.

### Build the Website

1. Create a copy of `AppConfig.py` from the `AppConfig.py.template` file in the `%project_dir%/src/config` folder.  
    * NOTE: This approach ensures local config settings are not committed by mistake. Any desired changes to the default configuration can be copied back to the `.template` file and committed.
2. Run `npm install` in your `%project_dir%`
3. Run `gulp build` to build the site for deployment.  
    * If you don't have gulp installed, run `npx gulp build` to execute from the node installation of gulp.
    * NOTE: Transpiled css and vendor js files are excluded from GIT

### Run the dev API backend

The API (opengamedata-website-api) should be running on <http://localhost:5000> in order to get Game Usage and Data Pipeline/Templates files list.

- See README in the [API repository](https://github.com/opengamedata/opengamedata-website-api) for further instructions.

Alternately, you may use an online instance of the File API.

- Ensure the following is commented out in the `src/config/AppConfig.py` file:

    ```py
    # If hostname starts with localhost
    if request.host in {'localhost', '127.0.0.1'}:
        # Assume we're in a development environment
        APP_CONFIG['WEBSITE_API_URL_BASE'] = 'http://localhost:5000/'
    ```

- Then set the `$APP_CONFIG['WEBSITE_API_URL_BASE']` line with a valid online path, such as the main instance hosted on `ogd-services`: <https://ogd-services.fielddaylab.wisc.edu/wsgi-bin/opengamedata/apis/files/app.wsgi/>

### Run the Website

There are a few options for running the website locally:

1. Run `flask run` in the `%project_dir%/src` folder to start Flask development server

    - Changes to scss are not automatically built to update the generated css files.

2. Run local Apache Server

    - TODO

### Debug with VS Code

Create a `.vscode/settings.json` in your local checkout, and add the following:

```json
{
   "files.associations": {
      "*.html": "jinja-html"
   },
}
```

Then, create `.vscode/launch.json` and add the following launch configuration:

```json
{
   // Use IntelliSense to learn about possible attributes.
   // Hover to view descriptions of existing attributes.
   // For more information, visit: https://go.microsoft.com/fwlink/?linkid=830387
   "version": "0.2.0",
   "configurations": [

      {
         "name": "Flask Debug",
         "type": "python",
         "request": "launch",
         "module": "flask",
         "cwd": "${workspaceFolder}/src",
         "env": {
            "FLASK_DEBUG": "1"
         },
         "args": [
            "run",
            "--no-debugger",
            "--no-reload"
         ],
         "jinja": true,
         "justMyCode": false
      }
   ]
}
```

You can now run the VS Code debugger, and load the pages in your local browser, with all the standard breakpoint and code-stepping features VS Code offers.
