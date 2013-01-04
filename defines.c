#define maxZoom 80.0
#define minZoom 15.0
#define initZoom 16.0

#define ZOOM_SPEED 0.15 
//#define zoomSpeed 6.0//lower is faster
#define focusSpeedMax 0.0500

#define FULL_SCREEN 0

//#define SCREEN_WIDTH 1280
//#define SCREEN_HEIGHT 960

//#define SCREEN_WIDTH 1024
//#define SCREEN_HEIGHT 768


#define SCREEN_WIDTH 1440
#define SCREEN_HEIGHT 900

//#define SCREEN_WIDTH 1600
//#define SCREEN_HEIGHT 1200

//#define SCREEN_WIDTH 1920
//#define SCREEN_HEIGHT 1200
#define SCREEN_BASE_WIDTH 1600
#define SCREEN_BASE_HEIGHT 1200

#define AUTO_CHOOSE_NEXT_DELAY 0

//#define SLIDE_UNIT_TIME 350
//#define SLIDE_UNIT_TIME 150.0
#define SLIDE_UNIT_TIME 10.0//put this back to 150 after debugging is done
#define AUTO_FOCUS_TIME_MAX 1000.0
#define AUTO_FOCUS_TIME_MIN 300.0

#define MAP_POSITION_FULL 0
#define MAP_POSITION_LEFT 1
#define MAP_POSITION_RIGHT 2

#define ANIMATION_UNIT_SLIDE 0
#define ANIMATION_AUTO_FOCUS 1
//#define ANIMATION_

#define ANIMATION_DAMAGE 0
#define ANIMATION_SELECTION_BOX 1
int animationTimes[2] = {4000,2000};

#define TILES "assets/tiles2.png"
#define UI "assets/UI.png"
#define TILE_SELECT_BOX "assets/tileSelect.png"
#define TILE_SELECT_BOX_INDEX 0

#define UI_MAP_EDITOR_TOP "assets/UITop.png"
#define UI_MAP_EDITOR_TOP_HEIGHT 100
#define UI_MAP_EDITOR_TOP_WIDTH 1600
#define UI_MAP_EDITOR_TOP_INDEX 1

#define UI_MAP_EDITOR_BOTTOM "assets/UIBottom.png"
#define UI_MAP_EDITOR_BOTTOM_HEIGHT 13
#define UI_MAP_EDITOR_BOTTOM_WIDTH 1600
#define UI_MAP_EDITOR_BOTTOM_INDEX 2

#define UI_MAP_EDITOR_LEFT "assets/UILeft.png"
#define UI_MAP_EDITOR_LEFT_HEIGHT 1089
#define UI_MAP_EDITOR_LEFT_WIDTH 286
#define UI_MAP_EDITOR_LEFT_INDEX 3

#define UI_MAP_EDITOR_RIGHT "assets/UIRight.png"
#define UI_MAP_EDITOR_RIGHT_HEIGHT 1089
#define UI_MAP_EDITOR_RIGHT_WIDTH 13
#define UI_MAP_EDITOR_RIGHT_INDEX 4

#define UI_NEW_GAME_SCREEN "assets/MenusBackground.png"
#define UI_NEW_GAME_SCREEN_HEIGHT 1200
#define UI_NEW_GAME_SCREEN_WIDTH 1600
#define UI_NEW_GAME_SCREEN_INDEX 5

#define CURSOR_POINTER "assets/cursors/gam372.png"
#define CURSOR_POINTER_INDEX 6

#define CURSOR_POINTER_ON "assets/cursors/gam375.png"
#define CURSOR_POINTER_ON_INDEX 7

#define CURSOR_MOVE "assets/cursors/gam378.png"
#define CURSOR_MOVE_INDEX 8

#define CURSOR_WIDTH 32
#define CURSOR_HEIGHT 32

#define PLAYER_START_BUTTON "assets/playerStartButton.png"
#define PLAYER_START_BUTTON_WIDTH 13
#define PLAYER_START_BUTTON_HEIGHT 14
#define PLAYER_START_BUTTON_INDEX 9

#define PLAYER_START "assets/playerStart.png"
#define PLAYER_START_WIDTH 13
#define PLAYER_START_HEIGHT 14
#define PLAYER_START_INDEX 10

#define UI_SCROLLABLE "assets/scrollableElement.png"
#define UI_SCROLLABLE_HEIGHT 404
#define UI_SCROLLABLE_WIDTH 210
#define UI_SCROLLABLE_INDEX 11

#define UI_SCROLL_PAD "assets/scrollPad.png"
#define UI_SCROLL_PAD_HEIGHT 16
#define UI_SCROLL_PAD_WIDTH 16
#define UI_SCROLL_PAD_INDEX 12
#define UI_SCROLL_PAD_DUMMY_HEIGHT 0
#define UI_SCROLL_PAD_DUMMY_WIDTH 0
#define UI_SCROLL_PAD_DUMMY_INDEX 12

#define UI_TEXT_INPUT "assets/textInput.png"
#define UI_TEXT_INPUT_HEIGHT 41
#define UI_TEXT_INPUT_WIDTH 304
#define UI_TEXT_INPUT_INDEX 13

#define MEEPLE "assets/meeple.png"
#define MEEPLE_HEIGHT 20
#define MEEPLE_WIDTH 200
#define MEEPLE_INDEX 14

#define HEALTH_BAR "assets/healthBar.png"
#define HEALTH_BAR_HEIGHT 6
#define HEALTH_BAR_WIDTH 52
#define HEALTH_BAR_INDEX 15

#define UNIT_BUILD_BAR "assets/unitBuildBar.png"
#define UNIT_BUILD_BAR_HEIGHT 12
#define UNIT_BUILD_BAR_WIDTH 180
#define UNIT_BUILD_BAR_INDEX 16

#define CITY_SANS_TREE "assets/citySansTree.png"
#define CITY_SANS_TREE_HEIGHT 96
#define CITY_SANS_TREE_WIDTH 98
#define CITY_SANS_TREE_INDEX 17

#define WALK_ICON "assets/walkIcon.png"
#define WALK_ICON_HEIGHT 36
#define WALK_ICON_WIDTH 36
#define WALK_ICON_INDEX 18

#define ADD_BUTTON "assets/addButton.png"
#define ADD_BUTTON_HEIGHT 20
#define ADD_BUTTON_WIDTH 20
#define ADD_BUTTON_INDEX 19

#define REMOVE_BUTTON "assets/removeButton.png"
#define REMOVE_BUTTON_HEIGHT 20
#define REMOVE_BUTTON_WIDTH 20
#define REMOVE_BUTTON_INDEX 20

#define CITY_VIEWER_BOX "assets/cityViewerBox.png"
#define CITY_VIEWER_BOX_HEIGHT 352
#define CITY_VIEWER_BOX_WIDTH 211
#define CITY_VIEWER_BOX_INDEX 21

#define UNIT_VIEWER_BOX "assets/unitViewerBox.png"
#define UNIT_VIEWER_BOX_HEIGHT 100
#define UNIT_VIEWER_BOX_WIDTH 211
#define UNIT_VIEWER_BOX_INDEX 22

#define UNIT_TYPE_VIEWER_BOX "assets/unitTypeViewerBox.png"
#define UNIT_TYPE_VIEWER_BOX_HEIGHT 241
#define UNIT_TYPE_VIEWER_BOX_WIDTH 211
#define UNIT_TYPE_VIEWER_BOX_INDEX 23

#define RESEARCH_BOX "assets/researchBox.png"
#define RESEARCH_BOX_HEIGHT 45
#define RESEARCH_BOX_WIDTH 190
#define RESEARCH_BOX_INDEX 24

#define SELECTION_BRACKET "assets/selectionBrackets.png"
#define SELECTION_BRACKET_HEIGHT 20
#define SELECTION_BRACKET_WIDTH 67
#define SELECTION_BRACKET_INDEX 25

#define ADD_BUTTON_SMALL "assets/addButtonSmall.png"
#define ADD_BUTTON_SMALL_HEIGHT 13
#define ADD_BUTTON_SMALL_WIDTH 13
#define ADD_BUTTON_SMALL_INDEX 26

#define REMOVE_BUTTON_SMALL "assets/removeButtonSmall.png"
#define REMOVE_BUTTON_SMALL_HEIGHT 13
#define REMOVE_BUTTON_SMALL_WIDTH 13
#define REMOVE_BUTTON_SMALL_INDEX 27

#define REMOVE_BUTTON_SMALL "assets/removeButtonSmall.png"
#define REMOVE_BUTTON_SMALL_HEIGHT 13
#define REMOVE_BUTTON_SMALL_WIDTH 13
#define REMOVE_BUTTON_SMALL_INDEX 27

#define UNIT_CIRCLE_RED "assets/selectionBoxRed.png"
#define UNIT_CIRCLE_RED_HEIGHT 40
#define UNIT_CIRCLE_RED_WIDTH 40
#define UNIT_CIRCLE_RED_INDEX 28

#define UNIT_CIRCLE_BLUE "assets/selectionBoxBlue.png"
#define UNIT_CIRCLE_BLUE_HEIGHT 40
#define UNIT_CIRCLE_BLUE_WIDTH 40
#define UNIT_CIRCLE_BLUE_INDEX 29

#define UNIT_CIRCLE_GREEN "assets/selectionBoxBlue.png"
#define UNIT_CIRCLE_GREEN_INDEX 30
#define UNIT_CIRCLE_YELLOW "assets/selectionBoxBlue.png"
#define UNIT_CIRCLE_YELLOW_INDEX 31
#define UNIT_CIRCLE_PINK "assets/selectionBoxBlue.png"
#define UNIT_CIRCLE_PINK_INDEX 32
#define UNIT_CIRCLE_ORANGE "assets/selectionBoxBlue.png"
#define UNIT_CIRCLE_ORANGE_INDEX 33
#define UNIT_CIRCLE_PURPLE "assets/selectionBoxBlue.png"
#define UNIT_CIRCLE_PURPLE_INDEX 34
#define UNIT_CIRCLE_BROWN "assets/selectionBoxBlue.png"
#define UNIT_CIRCLE_BROWN_INDEX 35

#define CURSOR_ATTACK "assets/cursors/swordIcon.png"
#define CURSOR_ATTACK_INDEX 36

#define CURSOR_HEAL "assets/cursors/healCursor.png"
#define CURSOR_HEAL_INDEX 37

#define ARCHER "assets/archer.png"
#define ARCHER_INDEX 38

#define SWORDSMAN "assets/swordsman.png"
#define SWORDSMAN_INDEX 39

#define SELECTION_BOX "assets/selectionBox.png"
#define SELECTION_BOX_INDEX 40

#define SUMMONER "assets/summoner.png"
#define SUMMONER_INDEX 41

#define CITY "assets/city.png"
#define CITY_INDEX 42

#define GATHERER "assets/gatherer.png"
#define GATHERER_INDEX 43

#define DRAGON "assets/dragon.png"
#define DRAGON_INDEX 44

#define WHITE_MAGE "assets/white_mage.png"
#define WHITE_MAGE_INDEX 45

#define WOLF "assets/wolf.png"
#define WOLF_INDEX 46

#define FIRE "assets/fire.png"
#define FIRE_INDEX 47

#define RED_MAGE "assets/red_mage.png"
#define RED_MAGE_INDEX 48

#define BLUE_MAGE "assets/blue_mage.png"
#define BLUE_MAGE_INDEX 49

#define ICE "assets/ice.png"
#define ICE_INDEX 50

#define GAME_FIND_BACKGROUND "assets/gameFindBackground.png"
#define GAME_FIND_BACKGROUND_HEIGHT 1200
#define GAME_FIND_BACKGROUND_WIDTH 1600
#define GAME_FIND_BACKGROUND_INDEX 51

//DEPRECATED
#define DEPRECATED "assets/GameFindMaps.png"
#define DEPRECATED_HEIGHT 978
#define DEPRECATED_WIDTH 1156
#define DEPRECATED_INDEX 52

#define ROOMS_DISPLAY "assets/roomsDisplay.png"
#define ROOMS_DISPLAY_HEIGHT 976
#define ROOMS_DISPLAY_WIDTH 1154
#define ROOMS_DISPLAY_INDEX 53

#define MODAL "assets/modal.png"
#define MODAL_HEIGHT 1200
#define MODAL_WIDTH 1600
#define MODAL_INDEX 54

#define OK_BUTTON "assets/okButton.png"
#define OK_BUTTON_HEIGHT 40
#define OK_BUTTON_WIDTH 97
#define OK_BUTTON_INDEX 55

#define MODAL_BACKGROUND "assets/modalBackground.png"
#define MODAL_BACKGROUND_HEIGHT 1200
#define MODAL_BACKGROUND_WIDTH 1600
#define MODAL_BACKGROUND_INDEX 56

#define MODAL_SMALL "assets/modalSmall.png"
#define MODAL_SMALL_HEIGHT 326
#define MODAL_SMALL_WIDTH 593
#define MODAL_SMALL_INDEX 57

#define SEND_BUTTON "assets/sendButton.png"
#define SEND_BUTTON_HEIGHT 32
#define SEND_BUTTON_WIDTH 62
#define SEND_BUTTON_INDEX 58

#define CHAT_BOX "assets/chatBox.png"
#define CHAT_BOX_HEIGHT 41
#define CHAT_BOX_WIDTH 304
#define CHAT_BOX_INDEX 59

#define CHAT_DISPLAY "assets/chatDisplay.png"
#define CHAT_DISPLAY_HEIGHT 912
#define CHAT_DISPLAY_WIDTH 304
#define CHAT_DISPLAY_INDEX 60

#define CREATE_GAME_BUTTON "assets/createGameButton.png"
#define CREATE_GAME_BUTTON_HEIGHT 33
#define CREATE_GAME_BUTTON_WIDTH 128
#define CREATE_GAME_BUTTON_INDEX 61

#define BACK_BUTTON "assets/backButton.png"
#define BACK_BUTTON_HEIGHT 33
#define BACK_BUTTON_WIDTH 85
#define BACK_BUTTON_INDEX 62

#define DA_1V1_BUTTON "assets/1v1Button.png"
#define DA_1V1_BUTTON_HEIGHT 32
#define DA_1V1_BUTTON_WIDTH 62
#define DA_1V1_BUTTON_INDEX 63

#define DA_2V2_BUTTON "assets/2v2Button.png"
#define DA_2V2_BUTTON_HEIGHT 32
#define DA_2V2_BUTTON_WIDTH 62
#define DA_2V2_BUTTON_INDEX 64

#define DA_3V3_BUTTON "assets/3v3Button.png"
#define DA_3V3_BUTTON_HEIGHT 32
#define DA_3V3_BUTTON_WIDTH 62
#define DA_3V3_BUTTON_INDEX 65

#define DA_4V4_BUTTON "assets/4v4Button.png"
#define DA_4V4_BUTTON_HEIGHT 32
#define DA_4V4_BUTTON_WIDTH 62
#define DA_4V4_BUTTON_INDEX 66

#define CREATE_GAME_BUTTON_LARGE "assets/createGameButtonLarge.png"
#define CREATE_GAME_BUTTON_LARGE_HEIGHT 41
#define CREATE_GAME_BUTTON_LARGE_WIDTH 168
#define CREATE_GAME_BUTTON_LARGE_INDEX 67

#define CREATE_GAME_BACKGROUND_LEFT "assets/createGameBackgroundLeft.png"
#define CREATE_GAME_BACKGROUND_LEFT_HEIGHT 824
#define CREATE_GAME_BACKGROUND_LEFT_WIDTH 544
#define CREATE_GAME_BACKGROUND_LEFT_INDEX 68

#define CREATE_GAME_BACKGROUND_RIGHT "assets/createGameBackgroundRight.png"
#define CREATE_GAME_BACKGROUND_RIGHT_HEIGHT 824
#define CREATE_GAME_BACKGROUND_RIGHT_WIDTH 65
#define CREATE_GAME_BACKGROUND_RIGHT_INDEX 69

#define CREATE_GAME_BACKGROUND_TOP "assets/createGameBackgroundTop.png"
#define CREATE_GAME_BACKGROUND_TOP_HEIGHT 118
#define CREATE_GAME_BACKGROUND_TOP_WIDTH 1600
#define CREATE_GAME_BACKGROUND_TOP_INDEX 70

#define CREATE_GAME_BACKGROUND_BOTTOM "assets/createGameBackgroundBottom.png"
#define CREATE_GAME_BACKGROUND_BOTTOM_HEIGHT 258
#define CREATE_GAME_BACKGROUND_BOTTOM_WIDTH 1600
#define CREATE_GAME_BACKGROUND_BOTTOM_INDEX 71

#define CREATE_GAME_BACKGROUND "assets/createGameBackground.png"
#define CREATE_GAME_BACKGROUND_HEIGHT 1200
#define CREATE_GAME_BACKGROUND_WIDTH 1600
#define CREATE_GAME_BACKGROUND_INDEX 72

#define MAP_SELECTOR "assets/mapSelector.png"
#define MAP_SELECTOR_HEIGHT 837
#define MAP_SELECTOR_WIDTH 454
#define MAP_SELECTOR_INDEX 73

#define JOIN_GAME_BACKGROUND "assets/joinRoomBackground.png"
#define JOIN_GAME_BACKGROUND_HEIGHT 1200
#define JOIN_GAME_BACKGROUND_WIDTH 1600
#define JOIN_GAME_BACKGROUND_INDEX 74

#define JOIN_GAME_CHAT "assets/joinRoomChat.png"
#define JOIN_GAME_CHAT_HEIGHT 540
#define JOIN_GAME_CHAT_WIDTH 454
#define JOIN_GAME_CHAT_INDEX 75

#define JOIN_GAME_CHAT_BOX "assets/joinRoomChatBox.png"
#define JOIN_GAME_CHAT_BOX_HEIGHT 41
#define JOIN_GAME_CHAT_BOX_WIDTH 454
#define JOIN_GAME_CHAT_BOX_INDEX 76

#define JOIN_GAME_PLAYERS "assets/joinRoomPlayers.png"
#define JOIN_GAME_PLAYERS_HEIGHT 177
#define JOIN_GAME_PLAYERS_WIDTH 454
#define JOIN_GAME_PLAYERS_INDEX 77

#define START_BUTTON "assets/startButton.png"
#define START_BUTTON_HEIGHT 40
#define START_BUTTON_WIDTH 97
#define START_BUTTON_INDEX 78

#define LOGIN_BUTTON "assets/loginButton.png"
#define LOGIN_BUTTON_HEIGHT 40
#define LOGIN_BUTTON_WIDTH 303
#define LOGIN_BUTTON_INDEX 79

#define SCROLL_BAR "assets/scrollBar.png"
#define SCROLL_BAR_HEIGHT 160
#define SCROLL_BAR_WIDTH 10
#define SCROLL_BAR_INDEX 80

#define UNIT_UI_BACK "assets/unitUIBack.png"
#define UNIT_UI_BACK_HEIGHT 70
#define UNIT_UI_BACK_WIDTH 311
#define UNIT_UI_BACK_INDEX 81

#define BUILD_BUTTON "assets/buildButton.png"
#define BUILD_BUTTON_HEIGHT 20
#define BUILD_BUTTON_WIDTH 68
#define BUILD_BUTTON_INDEX 82

#define UI_CITY_BACKGROUND "assets/UICityBackground.png"
#define UI_CITY_BACKGROUND_HEIGHT 1180
#define UI_CITY_BACKGROUND_WIDTH 358
#define UI_CITY_BACKGROUND_INDEX 83

#define UI_UNIT_BACKGROUND "assets/UIUnitBackground.png"
#define UI_UNIT_BACKGROUND_HEIGHT 1180
#define UI_UNIT_BACKGROUND_WIDTH 358
#define UI_UNIT_BACKGROUND_INDEX 84

#define MEDITATE_BUTTON "assets/meditateButton.png"
#define MEDITATE_BUTTON_HEIGHT 40
#define MEDITATE_BUTTON_WIDTH 136
#define MEDITATE_BUTTON_INDEX 85

#define MOVE_BUTTON "assets/moveButton.png"
#define MOVE_BUTTON_HEIGHT 27
#define MOVE_BUTTON_WIDTH 58
#define MOVE_BUTTON_INDEX 86

#define GREY_PEDESTAL "assets/greyPedestal.png"
#define GREY_PEDESTAL_HEIGHT 54
#define GREY_PEDESTAL_WIDTH 54
#define GREY_PEDESTAL_INDEX 87

#define CANCEL_MOVEMENT_BUTTON "assets/cancelMovementButton.png"
#define CANCEL_MOVEMENT_BUTTON_HEIGHT 40
#define CANCEL_MOVEMENT_BUTTON_WIDTH 244
#define CANCEL_MOVEMENT_BUTTON_INDEX 88

#define SKIP_BUTTON "assets/skipButton.png"
#define SKIP_BUTTON_HEIGHT 40
#define SKIP_BUTTON_WIDTH 97
#define SKIP_BUTTON_INDEX 89

#define START_GATHERING_BUTTON "assets/startGatheringButton.png"
#define START_GATHERING_BUTTON_HEIGHT 26
#define START_GATHERING_BUTTON_WIDTH 128
#define START_GATHERING_BUTTON_INDEX 90

#define BUILD_BORDER "assets/buildBorder.png"
#define BUILD_BORDER_HEIGHT 328
#define BUILD_BORDER_WIDTH 342
#define BUILD_BORDER_INDEX 91

#define RED_WOOD_ICON "assets/redWoodIcon.png"
#define RED_WOOD_ICON_HEIGHT 64
#define RED_WOOD_ICON_WIDTH 64
#define RED_WOOD_ICON_INDEX 92

#define BLUE_WOOD_ICON "assets/blueWoodIcon.png"
#define BLUE_WOOD_ICON_HEIGHT 64
#define BLUE_WOOD_ICON_WIDTH 64
#define BLUE_WOOD_ICON_INDEX 93

#define TIME_ICON "assets/timeIcon.png"
#define TIME_ICON_HEIGHT 64
#define TIME_ICON_WIDTH 64
#define TIME_ICON_INDEX 94

#define RESEARCH_BUTTON "assets/researchButton.png"
#define RESEARCH_BUTTON_HEIGHT 20
#define RESEARCH_BUTTON_WIDTH 68
#define RESEARCH_BUTTON_INDEX 95

#define RESEARCH_BORDER "assets/researchBorder.png"
#define RESEARCH_BORDER_HEIGHT 328
#define RESEARCH_BORDER_WIDTH 342
#define RESEARCH_BORDER_INDEX 96

#define QUEUE_BORDER "assets/queueBorder.png"
#define QUEUE_BORDER_HEIGHT 328
#define QUEUE_BORDER_WIDTH 342
#define QUEUE_BORDER_INDEX 97

#define CANCEL_BUTTON "assets/cancelButton.png"
#define CANCEL_BUTTON_HEIGHT 20
#define CANCEL_BUTTON_WIDTH 68
#define CANCEL_BUTTON_INDEX 98

#define UI_UNITTYPE_BACKGROUND "assets/uiUnitTypeBackground.png"
#define UI_UNITTYPE_BACKGROUND_HEIGHT 1084
#define UI_UNITTYPE_BACKGROUND_WIDTH 358
#define UI_UNITTYPE_BACKGROUND_INDEX 99

#define UI_CITYVIEW_BACKGROUND "assets/uiCityViewBackground.png"
#define UI_CITYVIEW_BACKGROUND_HEIGHT 810
#define UI_CITYVIEW_BACKGROUND_WIDTH 358
#define UI_CITYVIEW_BACKGROUND_INDEX 99

#define SLASH_ANIMATION "assets/slashAnim.png"
#define SLASH_ANIMATION_HEIGHT 2080
#define SLASH_ANIMATION_WIDTH 80
#define SLASH_ANIMATION_FRAME_COUNT 26
#define SLASH_ANIMATION_INDEX 100

#define TITLE "assets/title.png"
#define TITLE_HEIGHT 371
#define TITLE_WIDTH 577
#define TITLE_INDEX 101

#define MENU_BUTTON "assets/menuButton.png"
#define MENU_BUTTON_HEIGHT 33
#define MENU_BUTTON_WIDTH 33
#define MENU_BUTTON_INDEX 102

#define FLAG_POLE "assets/flagPole.png"
#define FLAG_POLE_INDEX 103

#define FLAG_TOP "assets/flagTop.png"
#define FLAG_TOP_INDEX 104

#define ARCHER_OVERLAY "assets/archerOverlay.png"
#define ARCHER_OVERLAY_INDEX 105

#define WHITE_MAGE_OVERLAY "assets/mageOverlay.png"
#define WHITE_MAGE_OVERLAY_INDEX 106

#define BLUE_MAGE_OVERLAY "assets/mageOverlay.png"
#define BLUE_MAGE_OVERLAY_INDEX 107

#define RED_MAGE_OVERLAY "assets/mageOverlay.png"
#define RED_MAGE_OVERLAY_INDEX 108

#define WOLF_OVERLAY "assets/wolfOverlay.png"
#define WOLF_OVERLAY_INDEX 109

#define DRAGON_OVERLAY "assets/dragonOverlay.png"
#define DRAGON_OVERLAY_INDEX 110

#define GATHERER_OVERLAY "assets/gathererOverlay.png"
#define GATHERER_OVERLAY_INDEX 111

#define CONNECT_BUTTON "assets/connectButton.png"
#define CONNECT_BUTTON_HEIGHT 40
#define CONNECT_BUTTON_WIDTH 303
#define CONNECT_BUTTON_INDEX 112

#define CHECK_MARK "assets/checkMark.png"
#define CHECK_MARK_HEIGHT 23
#define CHECK_MARK_WIDTH 26
#define CHECK_MARK_INDEX 113

#define CHECK_MARK_CHECKED "assets/checkMarkChecked.png"
#define CHECK_MARK_CHECKED_HEIGHT 23
#define CHECK_MARK_CHECKED_WIDTH 26
#define CHECK_MARK_CHECKED_INDEX 114

//DEPRECATED
#define CHECKBOXES_BACKGROUND "assets/checkBoxesBackground.png"
#define CHECKBOXES_BACKGROUND_HEIGHT 34
#define CHECKBOXES_BACKGROUND_WIDTH 222
#define CHECKBOXES_BACKGROUND_INDEX 115

#define UI_CITY_EDITOR_BACKGROUND_BACKGROUND "assets/uiCityEditorBackground.png"
#define UI_CITY_EDITOR_BACKGROUND_BACKGROUND_HEIGHT 1180
#define UI_CITY_EDITOR_BACKGROUND_BACKGROUND_WIDTH 358
#define UI_CITY_EDITOR_BACKGROUND_BACKGROUND_INDEX 116

#define MENU_MODAL "assets/menuModal.png"
#define MENU_MODAL_HEIGHT 1200
#define MENU_MODAL_WIDTH 1600
#define MENU_MODAL_INDEX 117

#define TILE_HEIGHT 500
#define TILE_WIDTH 433
#define TILE_INDEX_START 118

#define FOREST0 "assets/forest0.png"
#define FOREST_INDEX0 118
#define FOREST1 "assets/forest1.png"
#define FOREST_INDEX1 119
#define FOREST2 "assets/forest2.png"
#define FOREST_INDEX2 120
#define FOREST3 "assets/forest3.png"
#define FOREST_INDEX3 121

#define GRASS0 "assets/grass0.png"
#define GRASS_INDEX0 122
#define GRASS1 "assets/grass1.png"
#define GRASS_INDEX1 123
#define GRASS2 "assets/grass2.png"
#define GRASS_INDEX2 124
#define GRASS3 "assets/grass3.png"
#define GRASS_INDEX3 125

#define MOUNTAIN0 "assets/mountain0.png"
#define MOUNTAIN_INDEX0 126
#define MOUNTAIN1 "assets/mountain1.png"
#define MOUNTAIN_INDEX1 127
#define MOUNTAIN2 "assets/mountain2.png"
#define MOUNTAIN_INDEX2 128
#define MOUNTAIN3 "assets/mountain3.png"
#define MOUNTAIN_INDEX3 129

#define REDFOREST0 "assets/redforest0.png"
#define REDFOREST_INDEX0 130
#define REDFOREST1 "assets/redforest1.png"
#define REDFOREST_INDEX1 131
#define REDFOREST2 "assets/redforest2.png"
#define REDFOREST_INDEX2 132
#define REDFOREST3 "assets/redforest3.png"
#define REDFOREST_INDEX3 133

#define BLUEFOREST0 "assets/blueforest0.png"
#define BLUEFOREST_INDEX0 134
#define BLUEFOREST1 "assets/blueforest1.png"
#define BLUEFOREST_INDEX1 135
#define BLUEFOREST2 "assets/blueforest2.png"
#define BLUEFOREST_INDEX2 136
#define BLUEFOREST3 "assets/blueforest3.png"
#define BLUEFOREST_INDEX3 137

#define WATER0 "assets/water0.png"
#define WATER_INDEX0 138
#define WATER1 "assets/water1.png"
#define WATER_INDEX1 139
#define WATER2 "assets/water2.png"
#define WATER_INDEX2 140
#define WATER3 "assets/water3.png"
#define WATER_INDEX3 141

#define FLAG0 "assets/flag0.png"
#define FLAG_INDEX0 142
#define FLAG1 "assets/flag1.png"
#define FLAG_INDEX1 143
#define FLAG2 "assets/flag2.png"
#define FLAG_INDEX2 144
#define FLAG3 "assets/flag3.png"
#define FLAG_INDEX3 145

#define ADD_AI_BUTTON "assets/addAIButton.png"
#define ADD_AI_BUTTON_INDEX 146
#define ADD_AI_BUTTON_HEIGHT 40
#define ADD_AI_BUTTON_WIDTH 97

#define UNIT_VIEWER_BACKGROUND "assets/unitViewerBackground.png"
#define UNIT_VIEWER_BACKGROUND_INDEX 147
#define UNIT_VIEWER_BACKGROUND_HEIGHT 1180
#define UNIT_VIEWER_BACKGROUND_WIDTH 358

#define SUMMON_VIEWER_BACKGROUND "assets/summonViewerBackground.png"
#define SUMMON_VIEWER_BACKGROUND_INDEX 148
#define SUMMON_VIEWER_BACKGROUND_HEIGHT 1180
#define SUMMON_VIEWER_BACKGROUND_WIDTH 358

#define STONE_VIEWER_BACKGROUND "assets/stoneViewerBackground.png"
#define STONE_VIEWER_BACKGROUND_INDEX 149
#define STONE_VIEWER_BACKGROUND_HEIGHT 1180
#define STONE_VIEWER_BACKGROUND_WIDTH 358

#define BUILD "assets/build.png"
#define BUILD_INDEX 150
#define BUILD_HEIGHT 22
#define BUILD_WIDTH 64

#define SUMMON "assets/summon.png"
#define SUMMON_INDEX 151
#define SUMMON_HEIGHT 20
#define SUMMON_WIDTH 110

#define QUEUE "assets/queue.png"
#define QUEUE_INDEX 152
#define QUEUE_HEIGHT 25
#define QUEUE_WIDTH 78

#define FOREST_TILE_INDEX 0
#define GRASS_TILE_INDEX 1
#define MOUNTAIN_TILE_INDEX 2
#define RED_FOREST_TILE_INDEX 3
#define BLUE_FOREST_TILE_INDEX 4
#define WATER_TILE_INDEX 5
#define ROAD_TILE_INDEX 6
#define CITY_TILE_INDEX 7
#define PLAYER_START_TILE_INDEX 8

#define FOREST_MOVE_COST 1.0
#define GRASS_MOVE_COST 1.0
#define MOUNTAIN_MOVE_COST 999999.0
#define WATER_MOVE_COST 2.0

#define SIN60 0.86602540378
#define COS60 0.5

#define BUFSIZE 512

#define MAX_CITIES 40
#define MAX_CITY_NAME_LENGTH 50
#define MAX_UNITS 400
#define MAX_UNIT_NAME_LENGTH 50

#define WOOD_HIT_INDEX 0
#define WOOD_HIT "assets/audio/woodHit.ogg"
#define TUBE_HIT_INDEX 1
#define TUBE_HIT "assets/audio/sewageTubeHit.ogg"
#define DARBUKA_HIT_INDEX 2
#define DARBUKA_HIT "assets/audio/darbuka.ogg"
#define DARBUKA2_HIT_INDEX 3
#define DARBUKA2_HIT "assets/audio/darbuka2.ogg"
#define FINGER_CYMBALS_HIT_INDEX 4
#define FINGER_CYMBALS_HIT "assets/audio/fingerCymbals.ogg"
#define SWORD_HIT_INDEX 5
#define SWORD_HIT "assets/audio/swordHit.ogg"
#define DRAGON_FIRE_INDEX 5
#define DRAGON_FIRE "assets/audio/dragonFire.ogg"
#define BOW_HIT_INDEX 6
#define BOW_HIT "assets/audio/bowHit.ogg"

#define OMAR_1_INDEX 0
#define OMAR_1 "assets/audio/music/Omar Faruk Tekbilek - Whirling 01 Whirling Dervish.mp3"

#define OMAR_7_INDEX 1
#define OMAR_7 "assets/audio/music/Omar Faruk Tekbilek - Whirling 07 Caspian Winds.mp3"

#define EVENT_LEFT_CLICK_DOWN 0
#define EVENT_LEFT_CLICK_UP 1
#define EVENT_MOUSE_OVER 2
#define EVENT_MOUSE_MOVE 3
#define EVENT_SCROLL_UP 4
#define EVENT_SCROLL_DOWN 5
#define EVENT_RIGHT_CLICK_DOWN 6
#define EVENT_RIGHT_CLICK_UP 7
#define EVENT_KEY_DOWN 8
#define EVENT_KEY_UP 9
#define EVENT_ON_DRAW 10
#define EVENT_ON_QUIT 11
#define EVENT_SET_CURSOR_POSITION 12
#define EVENT_CHOOSE_NEXT_DELAYED 13
#define EVENT_POSITION_TEXT 14
#define EVENT_TEXT_OKAY 15

#define RENDERER_CHANGE_UNIT_ADD 0
#define RENDERER_CHANGE_UNIT_REMOVE 1
#define RENDERER_CHANGE_UNIT_CHANGE 2
#define RENDERER_CHANGE_NODE_CHANGE 3
#define RENDERER_CHANGE_TEXT_INPUT 4
#define RENDERER_SELECT_NEXT_UNIT 5
#define RENDERER_FOCUS 6
#define RENDERER_RESET_UNITS 7
#define RENDERER_RESET_UI 8 
#define RENDERER_ADD_UIELEM 9
#define RENDERER_REMOVE_UIELEM 10
#define RENDERER_UPDATE_UIELEM 11
#define RENDERER_RELOAD_MOVEPATH 12
#define RENDERER_RELOAD_ASTARPATH 13
#define RENDERER_SET_SELECTEDNODE 14
#define RENDERER_SET_BACKGROUND 15
#define RENDERER_LOAD_MAP 16
#define RENDERER_EXIT 17
#define RENDERER_CLICKSCROLL 18
#define RENDERER_SETVIEWPORTMODE 19
#define RENDERER_SETCHOOSENEXTDELAYED 20
#define RENDERER_LOADGAMEMODE 21

#define CREATE_GAME_ROOM_MODE 0
#define JOIN_GAME_ROOM_MODE 1
#define FULL_SCREEN_MODE 2
