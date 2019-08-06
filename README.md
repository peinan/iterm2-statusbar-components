# iTerm2 Status bar components
Components for iTerm2's status bar.

## Components

- [x] Weather Info
- [x] Disk Usage
- [x] Clock

## Install

- Enable iTerm2's Python API
- Install iTerm2's Python Runtime
- Install packages using **iTerm's pip**
- Set up the configs
- (Optional) Set up your fonts for a better look
- Run `make install`

### Enable iTerm2's Python API

Preference Panel: **General > Magic > Enable Python API**

### Install iTerm2's Python Runtime

Menubar: **Scripts > Manage > Install Python Runtime**

### Install packages using **iTerm2's pip**

Use **iTerm2's pip** to install required packages.

```bash
~/Library/Application Support/iTerm2/iterm2env/versions/3.7.2/bin/pip install -r requirements.txt
```

### Set up the configs

Create `config.json` in the `components` directory and set

- `PipPackagePath`: iTerm2's pip env path
- `OpenWeatherAPIKey`: (optional) OpenWeather API key

Example:

```config.json
{
  "PipPackagePath": "~/Library/Application Support/iTerm2/iterm2env-53/versions/3.7.2/lib/python3.7/site-packages",
  "OpenWeatherAPIKey": "xxxxx"
}
```

### (Optional) Set up your fonts for a better look

These components are using a lot of glyphs from [Nerd Fonts](https://github.com/ryanoasis/nerd-fonts).
So use the font with Nerd Fonts will bring you a better UI.

Change font from preference panel: **Profiles > Text > Font**

### Run `make install`

and it will create symbolic links.

## Usage

- Activate the component from menubar: **Scripts > AutoLaunch > [component]**
- Put the component to the position you like from preference panel: **Profiles > Session > Configure Status Bar**

