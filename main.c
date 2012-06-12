#include <stdio.h>
#include <stdlib.h>
#include <string.h>
#include <math.h>

#include <SDL.h>
#include <SDL_opengl.h>

#include <libpng12/png.h>
#include <Python/Python.h>

#include <ft2build.h>
#include <freetype/freetype.h>
#include <freetype/ftglyph.h>
#include <freetype/ftoutln.h>
#include <freetype/fttrigon.h>

PyObject *exc_type, *exc_value, *exc_traceback,*pyObj,*gameModule;
static void printPyStackTrace(){
  //put this thing after the call that is causing your problem!
    PyErr_Fetch(&exc_type, &exc_value, &exc_traceback);
    if(exc_type && exc_traceback){
      pyObj = PyObject_CallMethodObjArgs(gameModule,PyString_FromString("printTraceBack"),exc_type,exc_value,exc_traceback,NULL);
      if(pyObj != NULL){
	//Py_DECREF(pyObj);
      }
      PyErr_Print();//This is supposed to print it but doesn't. i left it here so the exception gets cleared...
    }
}
#include "fonts.h"

#define maxZoom 100.0
#define minZoom 1.0
#define initZoom 20.0

#define zoomSpeed 5.0//lower is faster
#define focusSpeed 5.0//lower is faster

#define FULL_SCREEN 0

#define SCREEN_WIDTH 1280
#define SCREEN_HEIGHT 960

//#define SCREEN_WIDTH 1024
//#define SCREEN_HEIGHT 768


//#define SCREEN_WIDTH 1440
//#define SCREEN_HEIGHT 900

//#define SCREEN_WIDTH 1600
//#define SCREEN_HEIGHT 1200

//#define SCREEN_WIDTH 1920
//#define SCREEN_HEIGHT 1200
#define SCREEN_BASE_WIDTH 1600
#define SCREEN_BASE_HEIGHT 1200

#define AUTO_CHOOSE_NEXT_DELAY 1500

#define TILES_IMAGE "assets/tiles2.png"
#define UI_IMAGE "assets/UI.png"
#define TILE_SELECT_BOX_IMAGE "assets/tileSelect.png"
#define TILE_SELECT_BOX_INDEX 0

#define UI_MAP_EDITOR_TOP_IMAGE "assets/UITop.png"
#define UI_MAP_EDITOR_TOP_IMAGE_HEIGHT 100
#define UI_MAP_EDITOR_TOP_IMAGE_WIDTH 1600
#define UI_MAP_EDITOR_TOP_INDEX 1

#define UI_MAP_EDITOR_BOTTOM_IMAGE "assets/UIBottom.png"
#define UI_MAP_EDITOR_BOTTOM_IMAGE_HEIGHT 13
#define UI_MAP_EDITOR_BOTTOM_IMAGE_WIDTH 1600
#define UI_MAP_EDITOR_BOTTOM_INDEX 2

#define UI_MAP_EDITOR_LEFT_IMAGE "assets/UILeft.png"
#define UI_MAP_EDITOR_LEFT_IMAGE_HEIGHT 1089
#define UI_MAP_EDITOR_LEFT_IMAGE_WIDTH 286
#define UI_MAP_EDITOR_LEFT_INDEX 3

#define UI_MAP_EDITOR_RIGHT_IMAGE "assets/UIRight.png"
#define UI_MAP_EDITOR_RIGHT_IMAGE_HEIGHT 1089
#define UI_MAP_EDITOR_RIGHT_IMAGE_WIDTH 13
#define UI_MAP_EDITOR_RIGHT_INDEX 4

#define UI_NEW_GAME_SCREEN_IMAGE "assets/MenusBackground.png"
#define UI_NEW_GAME_SCREEN_IMAGE_HEIGHT 1200
#define UI_NEW_GAME_SCREEN_IMAGE_WIDTH 1600
#define UI_NEW_GAME_SCREEN_INDEX 5

#define CURSOR_POINTER_IMAGE "assets/cursors/gam372.png"
#define CURSOR_POINTER_INDEX 6

#define CURSOR_POINTER_ON_IMAGE "assets/cursors/gam375.png"
#define CURSOR_POINTER_ON_INDEX 7

#define CURSOR_MOVE_IMAGE "assets/cursors/gam378.png"
#define CURSOR_MOVE_INDEX 8

#define CURSOR_WIDTH 32
#define CURSOR_HEIGHT 32

#define PLAYER_START_BUTTON_IMAGE "assets/playerStartButton.png"
#define PLAYER_START_BUTTON_WIDTH 13
#define PLAYER_START_BUTTON_HEIGHT 14
#define PLAYER_START_BUTTON_INDEX 9

#define PLAYER_START_IMAGE "assets/playerStart.png"
#define PLAYER_START_WIDTH 13
#define PLAYER_START_HEIGHT 14
#define PLAYER_START_INDEX 10

#define UI_SCROLLABLE_IMAGE "assets/scrollableElement.png"
#define UI_SCROLLABLE_IMAGE_HEIGHT 404
#define UI_SCROLLABLE_IMAGE_WIDTH 210
#define UI_SCROLLABLE_INDEX 11

#define UI_SCROLL_PAD "assets/scrollPad.png"
#define UI_SCROLL_PAD_HEIGHT 16
#define UI_SCROLL_PAD_WIDTH 16
#define UI_SCROLL_PAD_INDEX 12

#define UI_TEXT_INPUT_IMAGE "assets/textInput.png"
#define UI_TEXT_INPUT_IMAGE_HEIGHT 41
#define UI_TEXT_INPUT_IMAGE_WIDTH 304
#define UI_TEXT_INPUT_INDEX 13

#define MEEPLE_IMAGE "assets/meeple.png"
#define MEEPLE_IMAGE_HEIGHT 20
#define MEEPLE_IMAGE_WIDTH 200
#define MEEPLE_INDEX 14

#define HEALTH_BAR_IMAGE "assets/healthBar.png"
#define HEALTH_BAR_IMAGE_HEIGHT 6
#define HEALTH_BAR_IMAGE_WIDTH 52
#define HEALTH_BAR_INDEX 15

#define UNIT_BUILD_BAR_IMAGE "assets/unitBuildBar.png"
#define UNIT_BUILD_BAR_IMAGE_HEIGHT 12
#define UNIT_BUILD_BAR_IMAGE_WIDTH 180
#define UNIT_BUILD_BAR_INDEX 16

#define CITY_SANS_TREE_IMAGE "assets/citySansTree.png"
#define CITY_SANS_TREE_HEIGHT 96
#define CITY_SANS_TREE_WIDTH 98
#define CITY_SANS_TREE_INDEX 17

#define WALK_ICON_IMAGE "assets/walkIcon.png"
#define WALK_ICON_HEIGHT 36
#define WALK_ICON_WIDTH 36
#define WALK_ICON_INDEX 18

#define ADD_BUTTON_IMAGE "assets/addButton.png"
#define ADD_BUTTON_HEIGHT 20
#define ADD_BUTTON_WIDTH 20
#define ADD_BUTTON_INDEX 19

#define REMOVE_BUTTON_IMAGE "assets/removeButton.png"
#define REMOVE_BUTTON_HEIGHT 20
#define REMOVE_BUTTON_WIDTH 20
#define REMOVE_BUTTON_INDEX 20

#define CITY_VIEWER_BOX_IMAGE "assets/cityViewerBox.png"
#define CITY_VIEWER_BOX_HEIGHT 352
#define CITY_VIEWER_BOX_WIDTH 211
#define CITY_VIEWER_BOX_INDEX 21

#define UNIT_VIEWER_BOX_IMAGE "assets/unitViewerBox.png"
#define UNIT_VIEWER_BOX_HEIGHT 100
#define UNIT_VIEWER_BOX_WIDTH 211
#define UNIT_VIEWER_BOX_INDEX 22

#define UNIT_TYPE_VIEWER_BOX_IMAGE "assets/unitTypeViewerBox.png"
#define UNIT_TYPE_VIEWER_BOX_HEIGHT 241
#define UNIT_TYPE_VIEWER_BOX_WIDTH 211
#define UNIT_TYPE_VIEWER_BOX_INDEX 23

#define RESEARCH_BOX_IMAGE "assets/researchBox.png"
#define RESEARCH_BOX_HEIGHT 45
#define RESEARCH_BOX_WIDTH 190
#define RESEARCH_BOX_INDEX 24

#define SELECTION_BRACKET_IMAGE "assets/selectionBrackets.png"
#define SELECTION_BRACKET_HEIGHT 20
#define SELECTION_BRACKET_WIDTH 67
#define SELECTION_BRACKET_INDEX 25

#define ADD_BUTTON_SMALL_IMAGE "assets/addButtonSmall.png"
#define ADD_BUTTON_SMALL_HEIGHT 13
#define ADD_BUTTON_SMALL_WIDTH 13
#define ADD_BUTTON_SMALL_INDEX 26

#define REMOVE_BUTTON_SMALL_IMAGE "assets/removeButtonSmall.png"
#define REMOVE_BUTTON_SMALL_HEIGHT 13
#define REMOVE_BUTTON_SMALL_WIDTH 13
#define REMOVE_BUTTON_SMALL_INDEX 27

#define REMOVE_BUTTON_SMALL_IMAGE "assets/removeButtonSmall.png"
#define REMOVE_BUTTON_SMALL_HEIGHT 13
#define REMOVE_BUTTON_SMALL_WIDTH 13
#define REMOVE_BUTTON_SMALL_INDEX 27

#define UNIT_CIRCLE_RED_IMAGE "assets/selectionBoxRed.png"
#define UNIT_CIRCLE_RED_HEIGHT 40
#define UNIT_CIRCLE_RED_WIDTH 40
#define UNIT_CIRCLE_RED_INDEX 28

#define UNIT_CIRCLE_BLUE_IMAGE "assets/selectionBoxBlue.png"
#define UNIT_CIRCLE_BLUE_HEIGHT 40
#define UNIT_CIRCLE_BLUE_WIDTH 40
#define UNIT_CIRCLE_BLUE_INDEX 29

#define UNIT_CIRCLE_GREEN_IMAGE "assets/selectionBoxBlue.png"
#define UNIT_CIRCLE_GREEN_INDEX 30
#define UNIT_CIRCLE_YELLOW_IMAGE "assets/selectionBoxBlue.png"
#define UNIT_CIRCLE_YELLOW_INDEX 31
#define UNIT_CIRCLE_PINK_IMAGE "assets/selectionBoxBlue.png"
#define UNIT_CIRCLE_PINK_INDEX 32
#define UNIT_CIRCLE_ORANGE_IMAGE "assets/selectionBoxBlue.png"
#define UNIT_CIRCLE_ORANGE_INDEX 33
#define UNIT_CIRCLE_PURPLE_IMAGE "assets/selectionBoxBlue.png"
#define UNIT_CIRCLE_PURPLE_INDEX 34
#define UNIT_CIRCLE_BROWN_IMAGE "assets/selectionBoxBlue.png"
#define UNIT_CIRCLE_BROWN_INDEX 35

#define CURSOR_ATTACK_IMAGE "assets/cursors/swordIcon.png"
#define CURSOR_ATTACK_INDEX 36

#define CURSOR_HEAL_IMAGE "assets/cursors/healCursor.png"
#define CURSOR_HEAL_INDEX 37

#define ARCHER_IMAGE "assets/archer.png"
#define ARCHER_INDEX 38

#define SWORDSMAN_IMAGE "assets/swordsman.png"
#define SWORDSMAN_INDEX 39

#define SELECTION_BOX_IMAGE "assets/selectionBox.png"
#define SELECTION_BOX_INDEX 40

#define SUMMONER_IMAGE "assets/summoner.png"
#define SUMMONER_INDEX 41

#define CITY_IMAGE "assets/city.png"
#define CITY_INDEX 42

#define GATHERER_IMAGE "assets/gatherer.png"
#define GATHERER_INDEX 43

#define DRAGON_IMAGE "assets/dragon.png"
#define DRAGON_INDEX 44

#define WHITE_MAGE_IMAGE "assets/white_mage.png"
#define WHITE_MAGE_INDEX 45

#define WOLF_IMAGE "assets/wolf.png"
#define WOLF_INDEX 46

#define FIRE_IMAGE "assets/fire.png"
#define FIRE_INDEX 47

#define RED_MAGE_IMAGE "assets/red_mage.png"
#define RED_MAGE_INDEX 48

#define BLUE_MAGE_IMAGE "assets/blue_mage.png"
#define BLUE_MAGE_INDEX 49

#define ICE_IMAGE "assets/ice.png"
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

#define START_SUMMONING_BUTTON "assets/startSummoningButton.png"
#define START_SUMMONING_BUTTON_HEIGHT 27
#define START_SUMMONING_BUTTON_WIDTH 147
#define START_SUMMONING_BUTTON_INDEX 85

#define MOVE_BUTTON "assets/moveButton.png"
#define MOVE_BUTTON_HEIGHT 27
#define MOVE_BUTTON_WIDTH 58
#define MOVE_BUTTON_INDEX 86

#define GREY_PEDESTAL "assets/greyPedestal.png"
#define GREY_PEDESTAL_HEIGHT 54
#define GREY_PEDESTAL_WIDTH 54
#define GREY_PEDESTAL_INDEX 87

#define CANCEL_MOVEMENT_BUTTON "assets/cancelMovementButton.png"
#define CANCEL_MOVEMENT_BUTTON_HEIGHT 27
#define CANCEL_MOVEMENT_BUTTON_WIDTH 147
#define CANCEL_MOVEMENT_BUTTON_INDEX 88

#define SKIP_BUTTON "assets/skipButton.png"
#define SKIP_BUTTON_HEIGHT 27
#define SKIP_BUTTON_WIDTH 58
#define SKIP_BUTTON_INDEX 89

#define START_GATHERING_BUTTON "assets/startGatheringButton.png"
#define START_GATHERING_BUTTON_HEIGHT 26
#define START_GATHERING_BUTTON_WIDTH 128
#define START_GATHERING_BUTTON_INDEX 90

#define BUILD_BORDER "assets/buildBorder.png"
#define BUILD_BORDER_HEIGHT 328
#define BUILD_BORDER_WIDTH 342
#define BUILD_BORDER_INDEX 91

#define GREEN_WOOD_ICON "assets/greenWoodIcon.png"
#define GREEN_WOOD_ICON_HEIGHT 16
#define GREEN_WOOD_ICON_WIDTH 16
#define GREEN_WOOD_ICON_INDEX 92

#define BLUE_WOOD_ICON "assets/blueWoodIcon.png"
#define BLUE_WOOD_ICON_HEIGHT 16
#define BLUE_WOOD_ICON_WIDTH 16
#define BLUE_WOOD_ICON_INDEX 93

#define TIME_ICON "assets/timeIcon.png"
#define TIME_ICON_HEIGHT 16
#define TIME_ICON_WIDTH 16
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

#define SWORDSMAN_OVERLAY "assets/swordsmanOverlay.png"
#define SWORDSMAN_OVERLAY_INDEX 103

#define SUMMONER_OVERLAY "assets/summonerOverlay.png"
#define SUMMONER_OVERLAY_INDEX 104

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

#define FOREST_TILE_INDEX 0
#define GRASS_TILE_INDEX 1
#define MOUNTAIN_TILE_INDEX 2
#define RED_FOREST_TILE_INDEX 3
#define BLUE_FOREST_TILE_INDEX 4
#define WATER_TILE_INDEX 5
#define ROAD_TILE_INDEX 6
#define CITY_TILE_INDEX 7
#define PLAYER_START_TILE_INDEX 8

#define FOREST_MOVE_COST 2.0
#define GRASS_MOVE_COST 1.0
#define MOUNTAIN_MOVE_COST 999999.0
#define WATER_MOVE_COST 4.0

#define SIN60 0.8660
#define COS60 0.5

#define BUFSIZE 512

float screenRatio;
static SDL_Surface *gScreen;

int clickScroll = 0;
long doFocus = 0;
double focusXPos, focusYPos;
PyObject * pyFocusXPos;
PyObject * pyFocusYPos;
int isFocusing = 0;
int considerDoneFocusing = 0;
int leftButtonDown = 0;

int done = 0;    
int moveUp = 0;
int moveRight = 0;
int currentTick = 0;
int deltaTicks = 0;
int avgDeltaTicks = 0;
int totalDeltaTicksDataPoints = 0;

int keyHeld;
int repeatKey;
Uint32 keyHeldTime;

GLfloat mapDepth,mapDepthTest1,mapDepthTest2,mapDepthTest3;
float translateX = 0.0;
float translateY = 0.0;
float translateZ = 0.0-initZoom;
float translateXPrev = 0.0;
float translateYPrev = 0.0;
float translateZPrev = 0.0-initZoom;
//float translateZPrev2 = 0.0;
float scrollSpeed = 0.10;

PyObject * pyPolarity;
long mapPolarity;

GLdouble convertedBottomLeftX,convertedBottomLeftY,convertedBottomLeftZ;
GLdouble convertedTopRightX,convertedTopRightY,convertedTopRightZ;
GLdouble convertedCenterX,convertedCenterY,convertedCenterZ;

PyObject * pyUnitType;
PyObject * pyUnitTextureIndex;
PyObject * pyUnitTextureOverlayIndex;
PyObject * pyName;
PyObject * pyHealth;
PyObject * pyMaxHealth;
PyObject * pyLevel;
PyObject * pyPlayerNumber;
PyObject * pyRecentDamage;
PyObject * pyRecentDamageIter;
PyObject * pyDamageTime;
int damageTime;
PyObject * pyDamage;
char * damageStr;
char lvlStr[3];
char * unitName;
long playerNumber;
long unitTextureIndex;
long unitTextureOverlayIndex;
double healthBarLength;
PyObject * uiElement;
//PyObject * gameModule;
PyObject * gameState;
PyObject * gameMode;
PyObject * theMap;
PyObject * mapName;
PyObject * mapIterator;
PyObject * UIElementsIterator;
PyObject * rowIterator;
PyObject * pyMapWidth;
PyObject * pyMapHeight;
//PyObject * pyObj;
//PyObject * playableMode;
long mapWidth;
long mapHeight;

#define MAX_CITIES 40
#define MAX_CITY_NAME_LENGTH 50
#define MAX_UNITS 400
#define MAX_UNIT_NAME_LENGTH 50

/*float cityNamesXs[MAX_CITIES];
float cityNamesYs[MAX_CITIES];
char cityNames[MAX_CITIES][MAX_CITY_NAME_LENGTH];
int cityNamesCount = 0;
*/
/*float unitNamesXs[MAX_UNITS];
float unitNamesYs[MAX_UNITS];
char unitNames[MAX_UNITS][MAX_UNIT_NAME_LENGTH];
int unitNamesCount = 0;
*/
GLuint tilesTexture;
GLdouble mouseMapPosX, mouseMapPosY, mouseMapPosZ;
GLdouble mouseMapPosXPrevious, mouseMapPosYPrevious, mouseMapPosZPrevious = -initZoom;
GLint bufRenderMode;
float *textureVertices;
GLuint texturesArray[300];
GLuint tilesLists;
GLuint selectionBoxList;
GLuint unitList;
GLuint healthBarList;

int mouseX = 0;
int mouseY = 0;
GLuint selectBuf[BUFSIZE];

int selectedName = -1;//the mousedover object's 'name'
int previousClickedName = -2;
int previousMousedoverName = -2;
int theCursorIndex = -1;
float * vertexArrays[9];

float forestVertices[6][2] = {
  {(643.0/1280),1.0-(360.0/1280)},
  {(643.0/1280),1.0-(328.0/1280)},
  {(670.0/1280),1.0-(312.0/1280)},
  {(696.0/1280),1.0-(328.0/1280)},
  {(696.0/1280),1.0-(360.0/1280)},
  {(670.0/1280),1.0-(376.0/1280)}
};
float blueForestVertices[6][2] = {
  {(643.0/1280),1.0-(458.0/1280)},
  {(643.0/1280),1.0-(426.0/1280)},
  {(670.0/1280),1.0-(410.0/1280)},
  {(696.0/1280),1.0-(426.0/1280)},
  {(696.0/1280),1.0-(458.0/1280)},
  {(670.0/1280),1.0-(474.0/1280)}
};
float grassVertices[6][2] = {
  {(699.0/1280),1.0-(360.0/1280)},
  {(699.0/1280),1.0-(328.0/1280)},
  {(726.0/1280),1.0-(312.0/1280)},
  {(754.0/1280),1.0-(328.0/1280)},
  {(754.0/1280),1.0-(360.0/1280)},
  {(726.0/1280),1.0-(376.0/1280)}
};
float mountainVertices[6][2] = {
  {(699.0/1280),1.0-(556.0/1280)},
  {(699.0/1280),1.0-(524.0/1280)},
  {(726.0/1280),1.0-(508.0/1280)},
  {(754.0/1280),1.0-(524.0/1280)},
  {(754.0/1280),1.0-(556.0/1280)},
  {(726.0/1280),1.0-(572.0/1280)}
};
float waterVertices[6][2] = {
  {(874.0/1280),1.0-(850.0/1280)},
  {(874.0/1280),1.0-(818.0/1280)},
  {(901.0/1280),1.0-(802.0/1280)},
  {(928.0/1280),1.0-(818.0/1280)},
  {(928.0/1280),1.0-(850.0/1280)},
  {(901.0/1280),1.0-(866.0/1280)}
};
float roadVertices[6][2] = {
  {(467.0/1280),1.0-(66.0/1280)},
  {(467.0/1280),1.0-(34.0/1280)},
  {(494.0/1280),1.0-(18.0/1280)},
  {(522.0/1280),1.0-(34.0/1280)},
  {(522.0/1280),1.0-(66.0/1280)},
  {(494.0/1280),1.0-(82.0/1280)}
};
float cityVertices[6][2] = {
  {(641.0/1280),1.0-(66.0/1280)},
  {(641.0/1280),1.0-(34.0/1280)},
  {(668.0/1280),1.0-(18.0/1280)},
  {(696.0/1280),1.0-(34.0/1280)},
  {(696.0/1280),1.0-(66.0/1280)},
  {(668.0/1280),1.0-(82.0/1280)}
};
float playerStartVertices[6][2] = {
  {(593.0/1280),1.0-(556.0/1280)},
  {(593.0/1280),1.0-(524.0/1280)},
  {(610.0/1280),1.0-(508.0/1280)},
  {(638.0/1280),1.0-(524.0/1280)},
  {(638.0/1280),1.0-(556.0/1280)},
  {(610.0/1280),1.0-(572.0/1280)}
};

/*float hexagonVertices[6][2] = {
  //cheated these all out by 0.01 so the black background doesn't bleed through
  {-SIN60-0.01, -COS60-0.01},
  {-SIN60-0.01, COS60+0.01},
  {0.01, 1.01},
  {SIN60+0.01, COS60+0.01},
  {SIN60+0.01, -COS60-0.01},
  {0.01, -1.01}
  };*/
float hexagonVertices[6][2] = {
  //cheated these all out by 0.03 so the black background doesn't bleed through
  {-SIN60-0.02, -COS60-0.00},
  {-SIN60-0.02, COS60+0.00},
  {0.00, 1.00},
  {SIN60+0.02, COS60+0.00},
  {SIN60+0.02, -COS60-0.00},
  {0.00, -1.00}
};
float textureHexVertices[6][2] = {
  {0.0,0.25},
  {0.0,0.75},
  {0.5,1.0},
  {1.0,0.75},
  {1.0,0.25},
  {0.5,0.0}
};
/**************************** mouse hover object selection ********************************/
GLuint *bufferPtr,*ptrNames, numberOfNames;
int count;
int nameValue;
int namesCount;
int mouseTextPositionSet;
void processTheHits(GLint hitsCount, GLuint buffer[]){
  glFlush();
  count = 0;
  nameValue = 0;
  bufferPtr = (GLuint *) buffer;
  selectedName = -1;
  mouseTextPositionSet = 0;
  while(count < hitsCount){
    namesCount = 0;
    numberOfNames = *bufferPtr;
    //    nameValue = *(bufferPtr + 3);//the value of the name is stored +3 over in mem
    if(numberOfNames >= 1){
      //elements are created from back to front, the names should be in this order so we return the largest name
      while(namesCount < numberOfNames){
	nameValue = *(bufferPtr + 3 + namesCount);//the value of the name is stored +3 over in mem
	namesCount = namesCount + 1;
	if(nameValue > selectedName){
	  selectedName = nameValue;
	}
      }
      if(nameValue < 500){
	pyObj = PyObject_CallMethod(gameMode,"setMouseTextPosition","i",nameValue);
	Py_DECREF(pyObj);
	mouseTextPositionSet = 1;
      }
    }
    bufferPtr = bufferPtr + 3 + numberOfNames;
    count = count + 1;
  }  
  if(!mouseTextPositionSet){
	pyObj = PyObject_CallMethod(gameMode,"setMouseTextPosition","i",-1);
	if(pyObj != NULL){
    Py_DECREF(pyObj);
	}
  }
}

//float glMouseCoords[3];
//void convertWindowCoordsToViewportCoords(int x, int y){
GLint viewport[4];
GLdouble modelview[16];
GLdouble projection[16];
GLfloat winX, winY, winZ, winZOld;
void convertWindowCoordsToViewportCoords(int x, int y, float z, GLdouble* posX, GLdouble* posY, GLdouble* posZ){
  //strange things happen with this when zoom/maxZoom is greater than 45...
  glGetDoublev(GL_MODELVIEW_MATRIX,modelview);
  glGetDoublev(GL_PROJECTION_MATRIX,projection);
  glGetIntegerv(GL_VIEWPORT,viewport);//returns four values: the x and y window coordinates of the viewport, followed by its width and height.
  winX = (float)x;
  winY = SCREEN_HEIGHT - (float)y;
  gluUnProject( winX, winY, mapDepth, modelview, projection, viewport, posX, posY, posZ);
}
/**************************** /mouse hover object selection ********************************/

/************************************* drawing subroutines ***************************************/
float returnVal;
float translateTilesXToPositionX(int tileX,int tileY){
  //return (float)tilesX*-(1.9*SIN60);
  returnVal = (float)tileX*-(2.0*SIN60);
  if(abs(tileY)%2 == mapPolarity){
    returnVal += SIN60;
  }
  return returnVal;
}
float translateTilesYToPositionY(int tileY){
  return (float)(tileY*1.5);
}


int isNextUnit;
PyObject * pyUnit;
PyObject * pyFire;
PyObject * pyIce;
long isVisible;
void drawIce(){
  glBindTexture(GL_TEXTURE_2D, texturesArray[ICE_INDEX]);
  glCallList(unitList);
}
void drawFire(){
  glBindTexture(GL_TEXTURE_2D, texturesArray[FIRE_INDEX]);
  glCallList(unitList);
  double fireVitality;
  char fireVit[20];
  PyObject * pyFireVitality = PyObject_GetAttrString(pyFire,"vitality");
  fireVitality = PyFloat_AsDouble(pyFireVitality);
  glColor3f(1.0,1.0,1.0);
  glPushMatrix();
  glTranslatef(-0.8,0.0,0.0);
  glScalef(0.01,0.01,0.0);
  sprintf(fireVit,"%f",fireVitality);
  drawText(fireVit,0,-1,-9999.9,NULL);
  glPopMatrix();
  
}
void drawUnit(){
  pyUnitType = PyObject_GetAttrString(pyUnit,"unitType");
  pyUnitTextureIndex = PyObject_GetAttrString(pyUnitType,"textureIndex");
  pyUnitTextureOverlayIndex = PyObject_GetAttrString(pyUnitType,"overlayTextureIndex");
  pyName = PyObject_GetAttrString(pyUnitType,"name");
  unitName = PyString_AsString(pyName);
  pyHealth = PyObject_GetAttrString(pyUnit,"health");
  pyMaxHealth = PyObject_CallMethod(pyUnit,"getMaxHealth",NULL);
  pyLevel = PyObject_GetAttrString(pyUnit,"level");
  pyPlayerNumber = PyObject_GetAttrString(pyUnit,"player");
  playerNumber = PyLong_AsLong(pyPlayerNumber);
  unitTextureIndex = PyLong_AsLong(pyUnitTextureIndex);
  unitTextureOverlayIndex = PyLong_AsLong(pyUnitTextureOverlayIndex);
  healthBarLength = 1.5*PyFloat_AsDouble(pyHealth)/PyFloat_AsDouble(pyMaxHealth);
  pyRecentDamage = PyObject_GetAttrString(pyUnit,"recentDamage");
  pyRecentDamageIter = PyObject_GetIter(pyRecentDamage);
  glColor3f(1.0,1.0,1.0);
  if(isNextUnit == 1 && !isFocusing && isVisible){
    glBindTexture(GL_TEXTURE_2D, texturesArray[SELECTION_BOX_INDEX]);
    glCallList(selectionBoxList);
  }
  //else{
  //glBindTexture(GL_TEXTURE_2D, texturesArray[UNIT_CIRCLE_RED_INDEX+playerNumber-1]);
  //      }
  glBindTexture(GL_TEXTURE_2D, texturesArray[unitTextureIndex]);
  glCallList(unitList);
  if(playerNumber == 1){
    glColor3f(1.0,0.0,0.0);
  }else{
    glColor3f(0.0,0.0,1.0);
  }
  glBindTexture(GL_TEXTURE_2D, texturesArray[unitTextureOverlayIndex]);
  glCallList(unitList);
  glColor3f(1.0, 1.0, 1.0);
  glBindTexture(GL_TEXTURE_2D, texturesArray[HEALTH_BAR_INDEX]);
  glCallList(healthBarList);

  glColor3f(1.0, 0.0, 0.0);
  glBegin(GL_QUADS);
  glTexCoord2f(0.0,0.0);
  glVertex3f(-.75, 1.05, -0.001);
  glTexCoord2f(1.0,0.0);
  glVertex3f(-.75+healthBarLength, 1.05, -0.001);
  glTexCoord2f(1.0,1.0);
  glVertex3f(-.75+healthBarLength, 0.85, -0.001);
  glTexCoord2f(0.0,1.0);
  glVertex3f(-.75, 0.85, -0.001);
  glEnd();
  
  glColor3f(1.0, 1.0, 1.0);
  //printf("%ld",PyLong_AsLong(pyLevel));
  glPushMatrix();
  sprintf(lvlStr,"%ld",PyLong_AsLong(pyLevel));
  glTranslatef(-0.5,-0.7,-0.0001);
  glScalef(0.01,0.01,0.0);
  drawText(lvlStr,0,-1,-9999.9,NULL);
  glPopMatrix();

  while (pyDamageTime = PyIter_Next(pyRecentDamageIter)) {
    damageTime = PyLong_AsLong(pyDamageTime);
    if(currentTick-damageTime<200){
      glPushMatrix();
      glBindTexture(GL_TEXTURE_2D, texturesArray[SLASH_ANIMATION_INDEX]);
      glColor3f(1.0, 1.0, 1.0);
      float frameNumber = (((currentTick-damageTime)*SLASH_ANIMATION_FRAME_COUNT)/200)%SLASH_ANIMATION_FRAME_COUNT;
	  
      glBegin(GL_QUADS);	
      glTexCoord2f(1.0,(SLASH_ANIMATION_FRAME_COUNT-frameNumber-1)/SLASH_ANIMATION_FRAME_COUNT); glVertex3f(0.5,-0.5,0.0);
      glTexCoord2f(0.0,(SLASH_ANIMATION_FRAME_COUNT-frameNumber-1)/SLASH_ANIMATION_FRAME_COUNT); glVertex3f(-0.5,-0.5,0.0);
      glTexCoord2f(0.0,(SLASH_ANIMATION_FRAME_COUNT-frameNumber)/SLASH_ANIMATION_FRAME_COUNT); glVertex3f(-0.5,0.5,0.0);
      glTexCoord2f(1.0,(SLASH_ANIMATION_FRAME_COUNT-frameNumber)/SLASH_ANIMATION_FRAME_COUNT); glVertex3f(0.5,0.5,0.0);
      glEnd();
      glPopMatrix();
    }
    if(currentTick-damageTime<5000){
      glPushMatrix();
      pyDamage = PyObject_GetItem(pyRecentDamage,pyDamageTime);
      damageStr = PyString_AsString(pyDamage);
      int c = 0;
      while(damageStr[c] != 0){
	glTranslatef(-0.18,0.0,0.0);
	c++;
      }
      glColor4f(1.0, 0.0, 0.0, (5000.0-(currentTick-damageTime))/1000);
      glTranslatef(0.0,((currentTick-damageTime)*0.0002)-0.7,-0.0001);
      glScalef(0.01,0.01,0.0);
      drawText(damageStr,0,-1,-9999.9,NULL);
      glPopMatrix();
    }
  }

  Py_DECREF(pyUnitType);
  Py_DECREF(pyUnitTextureIndex);
  Py_DECREF(pyUnitTextureOverlayIndex);
  Py_DECREF(pyName);
  Py_DECREF(pyHealth);
  Py_DECREF(pyMaxHealth);
  Py_DECREF(pyLevel);
  Py_DECREF(pyPlayerNumber);
}
double xPosition;
double yPosition;
float shading;
char playerStartVal[2];
void drawTile(uint tilesXIndex, uint tilesYIndex, long name, long tileValue, long roadValue,char * cityName,long isSelected, long isOnMovePath,long playerStartValue, long cursorIndex){
  xPosition = translateTilesXToPositionX(tilesXIndex,tilesYIndex);
  yPosition = translateTilesYToPositionY(tilesYIndex);
  textureVertices = vertexArrays[tileValue];
  shading = 1.0;
  if(!isVisible){
    shading = shading - 0.5;
  }
  if(name == selectedName && !clickScroll){
    shading = shading - 0.4;
    if(cursorIndex >= 0){
      theCursorIndex = (int)cursorIndex;
    }
  }else if(isSelected == 1){
    shading = shading - 0.4;
  }
  glPushMatrix();
  glColor3f(shading,shading,shading);
  glTranslatef(xPosition,yPosition,0.0);

  glPushName(name);
  uint tileHash=0;
  tileHash += (((4294967296*(2654435761)*tilesXIndex)+81)%43261);
  tileHash += (((4294967296*(2654435761)*tilesYIndex)+30)%131071);
  tileHash = tileHash%4;
  glCallList(tilesLists+(4*tileValue)+tileHash);
  glPopName();

  if(roadValue == 1){
    glCallList(tilesLists+(4*ROAD_TILE_INDEX));
  }

  if(playerStartValue >= 1 && !PyObject_HasAttrString(gameMode,"units")){
    textureVertices = vertexArrays[PLAYER_START_TILE_INDEX];
    glCallList(tilesLists+(4*PLAYER_START_TILE_INDEX));
    sprintf(playerStartVal,"%ld",playerStartValue);

    glColor3f(1.0,1.0,1.0);
    glPushMatrix();
    glTranslatef(-0.4,0.3,0.0);
    glScalef(0.01,0.01,0.0);
    drawText(playerStartVal,0,-1,-9999.9,NULL);
    glPopMatrix();
  }

  if(pyUnit != NULL && pyUnit != Py_None && isVisible){
    drawUnit();
    glBindTexture(GL_TEXTURE_2D, texturesArray[CITY_SANS_TREE_INDEX]);
  }else{
    glBindTexture(GL_TEXTURE_2D, texturesArray[CITY_INDEX]);
  }
  
  if(cityName[0]!=0){
    glColor3f(1.0f, 1.0f, 1.0f);
    glBegin(GL_QUADS);
    glTexCoord2f(0.0,0.0);
    glVertex3f(-0.3, -0.3, 0.0);
    glTexCoord2f(1.0,0.0);
    glVertex3f(0.3, -0.3, 0.0);
    glTexCoord2f(1.0,1.0);
    glVertex3f(0.3, 0.3, 0.0);
    glTexCoord2f(0.0,1.0);
    glVertex3f(-0.3, 0.3, 0.0);
    glEnd();
    glEndList();
  }
  if(pyFire != NULL && pyFire != Py_None && isVisible){
    drawFire();
  }  
  if(isOnMovePath){
    glBindTexture(GL_TEXTURE_2D, texturesArray[WALK_ICON_INDEX]);
    glColor3f(1.0f, 0.0f, 0.0f);
    glBegin(GL_QUADS);
    glTexCoord2f(0.0,0.0); glVertex3f(0.5,-0.5,0.0);
    glTexCoord2f(1.0,0.0); glVertex3f(-0.5,-0.5,0.0);
    glTexCoord2f(1.0,1.0); glVertex3f(-0.5,0.5,0.0);
    glTexCoord2f(0.0,1.0); glVertex3f(0.5,0.5,0.0);
    glEnd();
    glBindTexture(GL_TEXTURE_2D, tilesTexture);
  }
  glPopMatrix();
}
void drawTilesText(){
  /*  int i,j,cityNameLength,unitNameLength = 0;
  for(i=0; i<cityNamesCount; i++){
    for(j=0; j<MAX_CITY_NAME_LENGTH; j++){
      if(cityNames[i][j] == 0){
	cityNameLength = j;
	break;
      }
    }
    glColor3f(1.0,1.0,1.0);
    glPushMatrix();
    glTranslatef(cityNamesXs[i]-(0.18*cityNameLength),cityNamesYs[i]+0.5,0.0);
    glScalef(0.010,0.010,0.0);
    drawText(cityNames[i],0,-9999.9,NULL);
    glPopMatrix();
  }
  cityNamesCount = 0;*/
  /*  for(i=0; i<unitNamesCount; i++){
    for(j=0; j<MAX_UNIT_NAME_LENGTH; j++){
      if(unitNames[i][j] == 0){
	unitNameLength = j;
	break;
      }
    }
    glColor3f(1.0,1.0,1.0);
    glPushMatrix();
    glTranslatef(unitNamesXs[i]-(0.3*j),unitNamesYs[i]+0.5,0.0);
    glScalef(0.009,0.009,0.0);
    drawText(unitNames[i],0,-9999.9,NULL);
    glPopMatrix();
  }
  unitNamesCount = 0;*/
}
int rowNumber;
PyObject * node;
PyObject * row;
int colNumber = 0;
PyObject * nodeIterator;
PyObject * nodeName;
PyObject * nodeValue;
PyObject * roadValue;
PyObject * pyCity;
PyObject * pyCursorIndex;
PyObject * pyPlayerStartValue;
PyObject * pyIsSelected;
PyObject * pyIsOnMovePath;
PyObject * pyIsVisible;
long longName;
long longValue;
long longRoadValue;
long cursorIndex;
PyObject * pyCityName;
char * cityName;
PyObject * nextUnit;
//PyObject * unit;
PyObject * pyUnitPlayer;
long unitPlayer;
long playerStartValue;
long isSelected;
long isOnMovePath;
void drawTiles(){
  rowNumber = -1;
  if(PyObject_HasAttrString(gameMode,"focusXPos")){
    pyFocusXPos = PyObject_GetAttrString(gameMode,"focusXPos");
    pyFocusYPos = PyObject_GetAttrString(gameMode,"focusYPos");
    focusXPos = PyLong_AsLong(pyFocusXPos);
    focusYPos = PyLong_AsLong(pyFocusYPos);
    focusXPos = translateTilesXToPositionX(0.0-focusXPos,focusYPos);
    focusYPos = translateTilesYToPositionY(focusYPos);
    Py_DECREF(pyFocusXPos);
    Py_DECREF(pyFocusYPos);
  }
  mapIterator = PyObject_CallMethod(theMap,"getIterator",NULL);
  pyPolarity = PyObject_GetAttrString(theMap,"polarity");
  mapPolarity = PyLong_AsLong(pyPolarity);
  rowIterator = PyObject_GetIter(mapIterator);
  while (row = PyIter_Next(rowIterator)) {
    colNumber = 0;
    rowNumber = rowNumber + 1;
    nodeIterator = PyObject_GetIter(row);
    while(node = PyIter_Next(nodeIterator)) {
      nodeName = PyObject_GetAttrString(node,"name");
      nodeValue = PyObject_CallMethod(node,"getValue",NULL);
      roadValue = PyObject_GetAttrString(node,"roadValue");
      pyCity = PyObject_GetAttrString(node,"city");
      pyCursorIndex = PyObject_GetAttrString(node,"cursorIndex");//New reference
      pyPlayerStartValue = PyObject_GetAttrString(node,"playerStartValue");//New reference                                 
      pyUnit = PyObject_GetAttrString(node,"unit");
      pyFire = PyObject_GetAttrString(node,"fire");
      pyIce = PyObject_GetAttrString(node,"ice");
      pyIsSelected = PyObject_GetAttrString(node,"selected");//New reference
      pyIsOnMovePath = PyObject_GetAttrString(node,"onMovePath");//New reference
      pyIsVisible = PyObject_GetAttrString(node,"visible");//New reference
      longName = PyLong_AsLong(nodeName);
      longValue = PyLong_AsLong(nodeValue);
      longRoadValue = PyLong_AsLong(roadValue);
      cursorIndex = PyLong_AsLong(pyCursorIndex);
      cityName = "";//TODO: REMOVE ME
      if(pyCity != Py_None){
	pyCityName = PyObject_GetAttrString(pyCity,"name");
	cityName = PyString_AsString(pyCityName);
      }
      isNextUnit = 0;
      nextUnit = PyObject_GetAttrString(gameMode,"nextUnit");
      if(pyUnit != NULL){
	if(pyUnit == nextUnit){
	  isNextUnit = 1;
	}
      }
      playerStartValue = PyLong_AsLong(pyPlayerStartValue);
      isSelected = PyLong_AsLong(pyIsSelected);
      isOnMovePath = PyLong_AsLong(pyIsOnMovePath);
      isVisible = PyLong_AsLong(pyIsVisible);
      Py_DECREF(nodeName);
      Py_DECREF(nodeValue);
      Py_DECREF(roadValue);
      Py_DECREF(pyCity);
      Py_DECREF(pyCursorIndex);
      Py_DECREF(pyPlayerStartValue);
      Py_DECREF(pyIsSelected);
      Py_DECREF(pyIsOnMovePath);
      if(pyIsVisible != NULL){
	Py_DECREF(pyIsVisible);
      }
      Py_DECREF(node);
      if(nextUnit != NULL){
      	Py_DECREF(nextUnit);
      }
      drawTile(colNumber,rowNumber,longName,longValue,longRoadValue,cityName,isSelected,isOnMovePath,playerStartValue,cursorIndex);
      colNumber = colNumber - 1;
      if(pyUnit != NULL){
	Py_DECREF(pyUnit);
      }
    }
    Py_DECREF(row);
    Py_DECREF(nodeIterator);
  }
  Py_DECREF(rowIterator); 
  Py_DECREF(mapIterator);
  Py_DECREF(pyPolarity);
}

void doViewport(){
  if(PyObject_HasAttrString(gameMode,"joinGameMode")){
    glViewport(60.0*SCREEN_WIDTH/SCREEN_BASE_WIDTH,258.0*SCREEN_HEIGHT/SCREEN_BASE_HEIGHT,991.5*SCREEN_WIDTH/SCREEN_BASE_WIDTH,824.0*SCREEN_HEIGHT/SCREEN_BASE_HEIGHT);
  }else if(PyObject_HasAttrString(gameMode,"createGameMode")){
    glViewport(544.0*SCREEN_WIDTH/SCREEN_BASE_WIDTH,258.0*SCREEN_HEIGHT/SCREEN_BASE_HEIGHT,991.5*SCREEN_WIDTH/SCREEN_BASE_WIDTH,824.0*SCREEN_HEIGHT/SCREEN_BASE_HEIGHT);
  }else{
    glViewport(0,0,SCREEN_WIDTH,SCREEN_HEIGHT);
  }
}
PyObject * pyTranslateZ;
float mapRightOffset;
float mapTopOffset;
int frameNumber = 0;
void calculateTranslation(){
  pyMapWidth = PyObject_CallMethod(theMap,"getWidth",NULL);//New reference
  pyMapHeight = PyObject_CallMethod(theMap,"getHeight",NULL);//New reference
  mapWidth = PyLong_AsLong(pyMapWidth);
  mapHeight = PyLong_AsLong(pyMapHeight);
  frameNumber++;
  glPushMatrix();
  if(theMap != NULL){
    pyTranslateZ = PyObject_GetAttrString(theMap,"translateZ");
    translateZ = PyFloat_AsDouble(pyTranslateZ);
  }
  if(translateX - mapRightOffset < convertedTopRightX
     && translateX - (2.0*SIN60) > convertedBottomLeftX
     && translateY < convertedTopRightY - mapTopOffset
     && translateY > convertedBottomLeftY+2.0
     && translateZ < translateZPrev){
    translateZ = translateZPrev;
    pyObj = PyObject_CallMethod(gameMode,"setMaxTranslateZ","f",translateZ);//New reference
    Py_DECREF(pyObj);
  }
  glTranslatef(translateX,translateY,translateZ);
  //glTranslatef(0.0,0.0,translateZ);
  glBindTexture(GL_TEXTURE_2D, texturesArray[OK_BUTTON_INDEX]);//draw a big texture for sampling map depth
  glBegin(GL_QUADS);
  glTexCoord2f(0.0,0.0); glVertex3f(-1000.0,-1000.0,0.0);
  glTexCoord2f(1.0,0.0); glVertex3f(1000.0,-1000.0,0.0);
  glTexCoord2f(1.0,1.0); glVertex3f(1000.0,1000.0,0.0);
  glTexCoord2f(0.0,1.0); glVertex3f(-1000.0,1000.0,0.0);
  glEnd();
  glPopMatrix();
  if(PyObject_HasAttrString(gameMode,"joinGameMode")){
    glReadPixels( 7*SCREEN_WIDTH/16, SCREEN_HEIGHT/2, 1, 1, GL_DEPTH_COMPONENT, GL_FLOAT, &mapDepthTest1 );
    glReadPixels( 8*SCREEN_WIDTH/16, SCREEN_HEIGHT/2, 1, 1, GL_DEPTH_COMPONENT, GL_FLOAT, &mapDepthTest2 );
    glReadPixels( 9*SCREEN_WIDTH/16, SCREEN_HEIGHT/2, 1, 1, GL_DEPTH_COMPONENT, GL_FLOAT, &mapDepthTest3 );
  }else if(PyObject_HasAttrString(gameMode,"createGameMode")){
    glReadPixels( 13*SCREEN_WIDTH/16, 7*SCREEN_HEIGHT/16, 1, 1, GL_DEPTH_COMPONENT, GL_FLOAT, &mapDepthTest1 );
    glReadPixels( 13*SCREEN_WIDTH/16, 8*SCREEN_HEIGHT/16, 1, 1, GL_DEPTH_COMPONENT, GL_FLOAT, &mapDepthTest2 );
    glReadPixels( 13*SCREEN_WIDTH/16, 9*SCREEN_HEIGHT/16, 1, 1, GL_DEPTH_COMPONENT, GL_FLOAT, &mapDepthTest3 );
  }else{
    glReadPixels( 7*SCREEN_WIDTH/16, SCREEN_HEIGHT/2, 1, 1, GL_DEPTH_COMPONENT, GL_FLOAT, &mapDepthTest1 );
    glReadPixels( 8*SCREEN_WIDTH/16, SCREEN_HEIGHT/2, 1, 1, GL_DEPTH_COMPONENT, GL_FLOAT, &mapDepthTest2 );
    glReadPixels( 9*SCREEN_WIDTH/16, SCREEN_HEIGHT/2, 1, 1, GL_DEPTH_COMPONENT, GL_FLOAT, &mapDepthTest3 );    
  }
  //  printf("%f %f %f\n",mapDepthTest1,mapDepthTest2,mapDepthTest3);
  if(mapDepthTest1 == mapDepthTest2 || mapDepthTest1 == mapDepthTest3){
    mapDepth = mapDepthTest1;
  }else if(mapDepthTest2 == mapDepthTest3){
    mapDepth = mapDepthTest2;
  }else{
    printf("mapdepth not found%d\n",1);
  }
  if(PyObject_HasAttrString(gameMode,"joinGameMode")){
    convertWindowCoordsToViewportCoords(60.0*SCREEN_WIDTH/SCREEN_BASE_WIDTH,SCREEN_HEIGHT,translateZ,&convertedBottomLeftX,&convertedBottomLeftY,&convertedBottomLeftZ);
    convertWindowCoordsToViewportCoords(1551.5*SCREEN_WIDTH/SCREEN_BASE_WIDTH,0.0,translateZ,&convertedTopRightX,&convertedTopRightY,&convertedTopRightZ);
  }else if(PyObject_HasAttrString(gameMode,"createGameMode")){
    convertWindowCoordsToViewportCoords(100.0*SCREEN_WIDTH/SCREEN_BASE_WIDTH,SCREEN_HEIGHT,translateZ,&convertedBottomLeftX,&convertedBottomLeftY,&convertedBottomLeftZ);
    convertWindowCoordsToViewportCoords(1535.5*SCREEN_WIDTH/SCREEN_BASE_WIDTH,0.0,translateZ,&convertedTopRightX,&convertedTopRightY,&convertedTopRightZ);
  }else{
    convertWindowCoordsToViewportCoords(390.0*SCREEN_WIDTH/SCREEN_BASE_WIDTH,SCREEN_HEIGHT,translateZ,&convertedBottomLeftX,&convertedBottomLeftY,&convertedBottomLeftZ);
    convertWindowCoordsToViewportCoords(SCREEN_WIDTH,0.0,translateZ,&convertedTopRightX,&convertedTopRightY,&convertedTopRightZ);
  }
  mouseMapPosXPrevious = mouseMapPosX;
  mouseMapPosYPrevious = mouseMapPosY;
  convertWindowCoordsToViewportCoords(mouseX,mouseY,translateZ,&mouseMapPosX,&mouseMapPosY,&mouseMapPosZ);  
  if(translateZ > translateZPrev){
    translateX = translateX + mouseMapPosX - mouseMapPosXPrevious;
    translateY = translateY + mouseMapPosY - mouseMapPosYPrevious;
  }
  translateZPrev = translateZ;
  //  convertWindowCoordsToViewportCoords(mouseX,mouseY,translateZ,&mouseMapPosXNew,&mouseMapPosYNew,&mouseMapPosZNew);
  mapRightOffset = translateTilesXToPositionX(mapWidth+1,0);
  mapTopOffset = translateTilesYToPositionY(mapHeight);
  //printf("screen topright %f,%f\n",convertedTopRightX,convertedTopRightY);
  //printf("screen bottomleft %f,%f\n",convertedBottomLeftX,convertedBottomLeftY);
  //printf("translate %f,%f,%f\n",translateX,translateY,translateZ);
  //printf("offsets: %f %f\n",mapRightOffset,mapTopOffset);
  //printf("%f\n",translateTilesYToPositionY(mapHeight));//setting translateY to this number will focus on it
  //printf("mouse %d:%f\t%d:%f\n",mouseX,mouseMapPosX,mouseY,mouseMapPosY);
  
  if(clickScroll > 0 && !isFocusing){
    translateX = translateX + mouseMapPosX - mouseMapPosXPrevious;
    translateY = translateY + mouseMapPosY - mouseMapPosYPrevious;
  }else if(!isFocusing){
    if(moveRight > 0){// && translateX > -10.0){
      translateX -= scrollSpeed*deltaTicks;
    }
    if(moveRight < 0){// && translateX < 10.0){
      translateX += scrollSpeed*deltaTicks;
    }
    if(moveUp > 0){// && translateY > -10.0){
      translateY -= scrollSpeed*deltaTicks;
    }
    if(moveUp < 0){// && translateY < 10.0){
      translateY += scrollSpeed*deltaTicks;
    }
  }
   if(isFocusing){
    //printf("%f %f %f %f\n",translateXPrev,translateX,translateYPrev,translateY);
    if((considerDoneFocusing == 1) && abs(50.0*(translateXPrev - translateX)) == 0 && abs(50.0*(translateYPrev - translateY)) == 0){//this indicates the auto-scrolling code is not allowing us to move any more
      isFocusing = 0;
      considerDoneFocusing = 0;
      if(PyObject_HasAttrString(gameMode,"onDoneFocusing")){
	pyObj = PyObject_CallMethod(gameMode,"onDoneFocusing",NULL);//New reference
	printPyStackTrace();
	Py_DECREF(pyObj);
      }
    }else if(abs(50.0*(translateXPrev - translateX)) == 0 && abs(50.0*(translateYPrev - translateY)) == 0){//this indicates the auto-scrolling code is not allowing us to move any more
      considerDoneFocusing = 1;
    }
    translateXPrev = translateX;
    translateYPrev = translateY;
    translateX = translateX-((translateX+focusXPos)/focusSpeed);
    translateY = translateY-((translateY+focusYPos)/focusSpeed);
   }
  //The following code will adjust translateX/Y so that no off-map area is shown
   //printf("%f\t%f\t%f\n",translateX,mapRightOffset,convertedBottomLeftX);
   if(translateX - mapRightOffset < convertedTopRightX){
    translateX = convertedTopRightX + mapRightOffset;
    if(translateX - (2.0*SIN60) > convertedBottomLeftX){
      //prevents shaking issue that occurs when the map is slightly larger than viewable area
      translateX = (convertedTopRightX + mapRightOffset + convertedBottomLeftX + (2.0*SIN60))/2.0;
    }
  }else if(translateX - (2.0*SIN60) > convertedBottomLeftX){
    translateX = convertedBottomLeftX + (2.0*SIN60);
    if(translateX - mapRightOffset < convertedTopRightX){
      //prevents shaking issue that occurs when the map is slightly larger than viewable area
      translateX = (convertedTopRightX + mapRightOffset + convertedBottomLeftX + (2.0*SIN60))/2.0;
    }
   }
   if(translateY < convertedTopRightY - mapTopOffset){
    translateY = convertedTopRightY - mapTopOffset;
    if(translateY > convertedBottomLeftY+2.0){
      //prevents shaking issue that occurs when the map is slightly larger than viewable area
      translateY = (convertedTopRightY-mapTopOffset+convertedBottomLeftY+2.0)/2.0;
    }
  }else if(translateY > convertedBottomLeftY+2.0){
    translateY = convertedBottomLeftY+2.0;
    if(translateY < convertedTopRightY - mapTopOffset){
      //prevents shaking issue that occurs when the map is slightly larger than viewable area
      translateY = (convertedTopRightY-mapTopOffset+convertedBottomLeftY+2.0)/2.0;
    }
   }
  if(theMap != Py_None && theMap != NULL){
    Py_DECREF(pyMapWidth);
    Py_DECREF(pyMapHeight);
  }
}

drawBoard(){
  if(theMap != Py_None && theMap != NULL){
    drawTiles();
    //    drawTilesText();
  }
}

void drawTileSelect(double xPos, double yPos, int name, long tileType, long selected){
  //THIS REALLY SHOULD HAVE BEEN DONE WITH uiElements...
  glLoadIdentity();
  glColor3f(1.0,1.0,1.0);
  glTranslatef(xPos,yPos,0.0);
  glScalef(0.01,0.01,0.0);
  glBindTexture(GL_TEXTURE_2D, tilesTexture);
  textureVertices = vertexArrays[tileType];
  glPushName(name);
  glBegin(GL_POLYGON);
  glTexCoord2f(*(textureVertices+0),*(textureVertices+1)); glVertex3f(3.0*hexagonVertices[0][0], 3.0*hexagonVertices[0][1], 0.0);
  glTexCoord2f(*(textureVertices+2),*(textureVertices+3)); glVertex3f(3.0*hexagonVertices[1][0], 3.0*hexagonVertices[1][1], 0.0);
  glTexCoord2f(*(textureVertices+4),*(textureVertices+5)); glVertex3f(3.0*hexagonVertices[2][0], 3.0*hexagonVertices[2][1], 0.0);
  glTexCoord2f(*(textureVertices+6),*(textureVertices+7)); glVertex3f(3.0*hexagonVertices[3][0], 3.0*hexagonVertices[3][1], 0.0);
  glTexCoord2f(*(textureVertices+8),*(textureVertices+9)); glVertex3f(3.0*hexagonVertices[4][0], 3.0*hexagonVertices[4][1], 0.0);
  glTexCoord2f(*(textureVertices+10),*(textureVertices+11)); glVertex3f(3.0*hexagonVertices[5][0], 3.0*hexagonVertices[5][1], 0.0);
  glEnd();
  glPopName();
  if(selected){
    glLoadIdentity();
    glTranslatef(xPos-0.04,yPos-0.04,0.0);
    glBindTexture(GL_TEXTURE_2D, texturesArray[TILE_SELECT_BOX_INDEX]);
    glBegin(GL_POLYGON);
    glTexCoord2f(1.0,1.0); glVertex3f(0.08,0.08,0.0);
    glTexCoord2f(1.0,0.0); glVertex3f(0.08,0.0,0.0);
    glTexCoord2f(0.0,0.0); glVertex3f(0.0,0.0,0.0);
    glTexCoord2f(0.0,1.0); glVertex3f(0.0,0.08,0.0);
    glEnd();
  }
}
int isNode;
unsigned int red[1],green[1],blue[1];
PyObject * pyXPosition;
PyObject * pyYPosition;
PyObject * pyWidth;
PyObject * pyHeight;
PyObject * pyHidden;
PyObject * pyName;
PyObject * pyTextureIndex;
PyObject * pyCursorIndex;
PyObject * pyText;
PyObject * pyQueuedText;
PyObject * pyRealText;
PyObject * pyLeftmostCharPosition;
PyObject * pyRightmostCharPosition;
PyObject * pyRecalculateText;
PyObject * pyDecrementMe;
PyObject * pyTextColor;
PyObject * pyTextSize;
PyObject * pyColor;
PyObject * pyMouseOverColor;
PyObject * pyTextXPosition;
PyObject * pyTextYPosition;
PyObject * pyCursorPosition;
PyObject * pyFontIndex;
PyObject * pyFrameLength;
PyObject * pyFrameCount;
PyObject * pyIsFocused;
//double xPosition;
//double yPosition;
double width;
double height;
int hidden;
long name;
long textureIndex;
long cursorIndex;
char * text;
int wordWidth;
char * queuedText;
char * realText;
int leftmostCharPosition;
int rightmostCharPosition;
int recalculateText;
char * textColor;
double textSize;
char * color;
char * mouseOverColor;
double textXPosition;
double textYPosition;
double cursorPosition;
double fontIndex;
int frameLength;
int frameCount;
int isFocused;

void drawUIElement(PyObject * uiElement){
  isNode = PyObject_HasAttrString(uiElement,"tileValue");
  if(!isNode){
    pyXPosition = PyObject_GetAttrString(uiElement,"xPosition");
    pyYPosition = PyObject_GetAttrString(uiElement,"yPosition");
    pyWidth = PyObject_GetAttrString(uiElement,"width");
    pyHeight = PyObject_GetAttrString(uiElement,"height");
    pyHidden = PyObject_GetAttrString(uiElement,"hidden");
    pyName = PyObject_GetAttrString(uiElement,"name");
    pyTextureIndex = PyObject_GetAttrString(uiElement,"textureIndex");
    pyCursorIndex = PyObject_GetAttrString(uiElement,"cursorIndex");
    pyText = PyObject_GetAttrString(uiElement,"text");
    pyTextColor = PyObject_GetAttrString(uiElement,"textColor");
    pyTextSize = PyObject_GetAttrString(uiElement,"textSize");
    pyColor = PyObject_GetAttrString(uiElement,"color");
    pyMouseOverColor = PyObject_GetAttrString(uiElement,"mouseOverColor");
    pyTextXPosition = PyObject_GetAttrString(uiElement,"textXPos");
    pyTextYPosition = PyObject_GetAttrString(uiElement,"textYPos");
    pyCursorPosition = PyObject_GetAttrString(uiElement,"cursorPosition");
    pyFontIndex = PyObject_GetAttrString(uiElement,"fontIndex");
    pyFrameLength = PyObject_GetAttrString(uiElement,"frameLength");
    pyFrameCount = PyObject_GetAttrString(uiElement,"frameCount");
    pyIsFocused = PyObject_GetAttrString(uiElement,"focused");

    xPosition = PyFloat_AsDouble(pyXPosition);
    yPosition = PyFloat_AsDouble(pyYPosition);
    width = PyFloat_AsDouble(pyWidth);
    height = PyFloat_AsDouble(pyHeight);
    hidden = pyHidden==Py_True;
    name = PyLong_AsLong(pyName);
    textureIndex = PyLong_AsLong(pyTextureIndex);
    cursorIndex = PyLong_AsLong(pyCursorIndex);
    text = PyString_AsString(pyText);
    textColor = PyString_AsString(pyTextColor);
    textSize = PyFloat_AsDouble(pyTextSize);
    color = PyString_AsString(pyColor);
    mouseOverColor = PyString_AsString(pyMouseOverColor);
    textXPosition = PyFloat_AsDouble(pyTextXPosition);
    textYPosition = PyFloat_AsDouble(pyTextYPosition);
    cursorPosition = PyFloat_AsDouble(pyCursorPosition);
    fontIndex = PyFloat_AsDouble(pyFontIndex);
    frameLength = PyLong_AsLong(pyFrameLength);
    frameCount = PyLong_AsLong(pyFrameCount);
    isFocused = pyIsFocused==Py_True;
     
    Py_DECREF(pyXPosition);
    Py_DECREF(pyYPosition);
    Py_DECREF(pyWidth);
    Py_DECREF(pyHeight);
    Py_DECREF(pyHidden);
    Py_DECREF(pyName);
    Py_DECREF(pyTextureIndex);
    Py_DECREF(pyCursorIndex);
    Py_DECREF(pyText);
    Py_DECREF(pyTextColor);
    Py_DECREF(pyTextSize);
    Py_DECREF(pyColor);
    Py_DECREF(pyMouseOverColor);
    Py_DECREF(pyTextXPosition);
    Py_DECREF(pyTextYPosition);
    Py_DECREF(pyCursorPosition);
    Py_DECREF(pyFontIndex);
    Py_DECREF(pyFrameLength);
    Py_DECREF(pyFrameCount);
    Py_DECREF(pyIsFocused);

    if(previousMousedoverName != selectedName){
      if(PyObject_HasAttrString(gameMode,"handleMouseOver")){
	pyObj = PyObject_CallMethod(gameMode,"handleMouseOver","(ii)",selectedName,leftButtonDown);//New reference
	printPyStackTrace();
	Py_DECREF(pyObj);
      }
      previousMousedoverName = selectedName;
    }
    if(!hidden){
      if(PyObject_HasAttrString(uiElement,"tileType")){//gameModeTileSelectButton
	drawTileSelect(xPosition,yPosition,name,PyLong_AsLong(PyObject_GetAttrString(uiElement,"tileType")),PyLong_AsLong(PyObject_GetAttrString(uiElement,"selected")));
      }else{
	if(textureIndex > -1){
	  glPushMatrix();
	  glLoadIdentity();
	  glBindTexture(GL_TEXTURE_2D, texturesArray[textureIndex]);
	  sscanf(color,"%X %X %X",red,green,blue);
	  //	glColor3f(red1.0f, 1.0f, 1.0f);
	  glColor3f(*red/255.0, *green/255.0, *blue/255.0);
	  glPushName(name);
	  glBegin(GL_QUADS);
	  if(frameCount > 1){
	    float frameNumber = frameCount-1-(currentTick/frameLength)%frameCount;
	    glTexCoord2f(0.0,(frameNumber/frameCount)+1.0/frameCount); glVertex3f(xPosition,yPosition,0.0);
	    glTexCoord2f(1.0,(frameNumber/frameCount)+1.0/frameCount); glVertex3f(xPosition+width,yPosition,0.0);
	    glTexCoord2f(1.0,(frameNumber/frameCount)); glVertex3f(xPosition+width,yPosition-height,0.0);
	    glTexCoord2f(0.0,(frameNumber/frameCount)); glVertex3f(xPosition,yPosition-height,0.0);
	  }else{
	    glTexCoord2f(0.0,1.0); glVertex3f(xPosition,yPosition,0.0);
	    glTexCoord2f(1.0,1.0); glVertex3f(xPosition+width,yPosition,0.0);
	    glTexCoord2f(1.0,0.0); glVertex3f(xPosition+width,yPosition-height,0.0);
	    glTexCoord2f(0.0,0.0); glVertex3f(xPosition,yPosition-height,0.0);
	  }
	  glEnd();
	  glPopName();
	  glPopMatrix();
	}
	if(PyObject_HasAttrString(uiElement,"realText")){
	  pyRecalculateText = PyObject_GetAttrString(uiElement,"recalculateText");
	  recalculateText = PyLong_AsLong(pyRecalculateText);
	  if(recalculateText){
	    pyRealText = PyObject_GetAttrString(uiElement,"realText");
	    pyLeftmostCharPosition = PyObject_GetAttrString(uiElement,"leftmostCharPosition");
	    pyRightmostCharPosition = PyObject_GetAttrString(uiElement,"rightmostCharPosition");
	    leftmostCharPosition = PyLong_AsLong(pyLeftmostCharPosition);
	    rightmostCharPosition = PyLong_AsLong(pyRightmostCharPosition);
	    realText = PyString_AsString(pyRealText);
	    glPushMatrix();
	    glLoadIdentity();
	    glTranslatef(xPosition+textXPosition,yPosition+textYPosition,0.0);
	    glScalef(textSize,textSize,0.0);
	    findTextWidth(uiElement,fontIndex,realText,xPosition+width,leftmostCharPosition,rightmostCharPosition,cursorPosition,recalculateText);
	    glPopMatrix();
	    Py_DECREF(pyLeftmostCharPosition);
	    Py_DECREF(pyRightmostCharPosition);
	    Py_DECREF(pyRealText);
	  }
	  Py_DECREF(pyRecalculateText);	  
	}
	//      printf("index: %ld %ld %f %f %f %f\n",name,textureIndex,xPosition,yPosition,width,height);
	if(PyObject_HasAttrString(uiElement,"textQueue")){
	  pyQueuedText = PyObject_CallMethod(uiElement,"getText",NULL);
	  queuedText = PyString_AsString(pyQueuedText);
	  if(queuedText[0] != 0){
	    glPushMatrix();
	    glLoadIdentity();
	    glTranslatef(xPosition+textXPosition,yPosition+textYPosition,0.0);
	    glScalef(textSize,textSize,0.0);
	    wordWidth = findWordWidth(fontIndex,queuedText,xPosition+width);
	    glPopMatrix();
	    pyDecrementMe = PyObject_CallMethod(uiElement,"addLine","i",wordWidth);
	    
	    //	    printf("%s\n",queuedText);
	  }
	  Py_DECREF(pyQueuedText);
	}
	if(PyObject_HasAttrString(uiElement,"text")){
	  glColor3f(*red/255.0, *green/255.0, *blue/255.0);
	  if(selectedName == name){
	    sscanf(mouseOverColor,"%X %X %X",red,green,blue);
	  }else{
	    sscanf(textColor,"%X %X %X",red,green,blue);
	  }
	  glColor3f(*red/255.0, *green/255.0, *blue/255.0);
	  glPushMatrix();
	  glLoadIdentity();
	  glTranslatef(xPosition+textXPosition,yPosition+textYPosition,0.0);
	  glScalef(textSize,textSize,0.0);
	  //glTranslatef(0.0,0.0,-10.0);
	  glPushName(name);
	  if(isFocused){
	    drawText(text,fontIndex,cursorPosition,xPosition+width,NULL);
	  }else{
	    drawText(text,fontIndex,-1,xPosition+width,NULL);
	  }	    
	  glPopName();
	  glPopMatrix();
	}
      }
      Py_DECREF(uiElement);
      if(name == selectedName && cursorIndex >= 0){
	theCursorIndex = cursorIndex;
      }
    }
  }
}
float xPos;
float yPos;
float pointerWidth;
float pointerHeight;
char frameRate[20];
void drawUI(){
  pyObj = PyObject_CallMethod(gameMode,"getUIElementsIterator",NULL);
  if(pyObj != NULL){
	  UIElementsIterator = PyObject_GetIter(pyObj);//New reference
	  while (uiElement = PyIter_Next(UIElementsIterator)) {
		drawUIElement(uiElement);
	  }
	  Py_DECREF(UIElementsIterator);
	  Py_DECREF(pyObj);
  }
  glGetIntegerv(GL_RENDER_MODE,&bufRenderMode);
  if(bufRenderMode==GL_RENDER){//need to hide the cursor during GL_SELECT
    /*draw cursor*/
    glPushMatrix();
    glLoadIdentity();
    if(theCursorIndex >= 0){
      glBindTexture(GL_TEXTURE_2D, texturesArray[theCursorIndex]);
    }else{
      glBindTexture(GL_TEXTURE_2D, texturesArray[CURSOR_POINTER_INDEX]);
    }
    glColor3f(1.0,1.0,1.0);
    glBegin(GL_QUADS);
    xPos = (mouseX/(SCREEN_WIDTH/2.0))-1.0;
    yPos = 1.0-(mouseY/(SCREEN_HEIGHT/2.0));
    pointerWidth = 2.0*CURSOR_WIDTH/SCREEN_WIDTH;
    pointerHeight = 2.0*CURSOR_HEIGHT/SCREEN_HEIGHT;
    
    glTexCoord2f(0.0,1.0); glVertex3f(xPos,yPos,0.0);
    glTexCoord2f(1.0,1.0); glVertex3f(xPos+pointerWidth,yPos,0.0);
    glTexCoord2f(1.0,0.0); glVertex3f(xPos+pointerWidth,yPos-pointerHeight,0.0);
    glTexCoord2f(0.0,0.0); glVertex3f(xPos,yPos-pointerHeight,0.0);
    glEnd();
    glPopMatrix();
  }

  /*frame rate display*/
  if(deltaTicks != 0){
    
    avgDeltaTicks = ((avgDeltaTicks*totalDeltaTicksDataPoints) + deltaTicks)/(totalDeltaTicksDataPoints+1);
    totalDeltaTicksDataPoints = totalDeltaTicksDataPoints + 1;
    sprintf(frameRate,"%ld",(long)(1000.0/avgDeltaTicks));
    glPushMatrix();
    glColor3f(1.0,1.0,1.0);
    glLoadIdentity();
    glTranslatef(-1.0,-1.0,0.0);
    glScalef(0.0005,0.0005,0.0);
    drawText(frameRate,0,-1,-9999.9,NULL);
    glPopMatrix();
    if(totalDeltaTicksDataPoints > 100){
      avgDeltaTicks = 0;
      totalDeltaTicksDataPoints = 0;
    }

  }
}
/************************************* /drawing subroutines ***************************************/

/************************************** opengl init **************************************/
static void initGL (){
  /** needs to be called on screen resize **/
  //unneeded with sdl?

  glViewport(0, 0, SCREEN_WIDTH, SCREEN_HEIGHT);//default values anyway, so not needed but w/e
  glInitNames(); //init names stack	
  glClearColor(0.0, 0.0, 0.0, 0.0); //sets screen clear color

  //glClearColor(1.0, 1.0, 1.0, 1.0); //sets screen clear color
  //glClearColor(123.0/255.0,126.0/255.0,125.0/255.0,1.0);//grey that matches the UI...
  glClearDepth(0.0);
  //glAlphaFunc(GL_GREATER,0.5);//clear area around the fonts will not write to the z-buffer
  glEnable(GL_ALPHA_TEST);
  glEnable(GL_DEPTH_TEST);
  glEnable(GL_TEXTURE_2D);
  glEnable(GL_BLEND);
  glBlendFunc(GL_SRC_ALPHA, GL_ONE_MINUS_SRC_ALPHA);     
  //  glDepthFunc(GL_ALWAYS);    
  //  glDepthFunc(GL_LEQUAL);
  screenRatio = (GLfloat)SCREEN_WIDTH/(GLfloat)SCREEN_HEIGHT;

  pngLoad(&tilesTexture, TILES_IMAGE);	/******************** /image init ***********************/
  pngLoad(&texturesArray[TILE_SELECT_BOX_INDEX],TILE_SELECT_BOX_IMAGE);
  pngLoad(&texturesArray[UI_MAP_EDITOR_TOP_INDEX],UI_MAP_EDITOR_TOP_IMAGE);
  pngLoad(&texturesArray[UI_MAP_EDITOR_BOTTOM_INDEX],UI_MAP_EDITOR_BOTTOM_IMAGE);
  pngLoad(&texturesArray[UI_MAP_EDITOR_LEFT_INDEX],UI_MAP_EDITOR_LEFT_IMAGE);
  pngLoad(&texturesArray[UI_MAP_EDITOR_RIGHT_INDEX],UI_MAP_EDITOR_RIGHT_IMAGE);
  pngLoad(&texturesArray[UI_NEW_GAME_SCREEN_INDEX],UI_NEW_GAME_SCREEN_IMAGE);
  pngLoad(&texturesArray[CURSOR_POINTER_INDEX],CURSOR_POINTER_IMAGE);
  pngLoad(&texturesArray[CURSOR_POINTER_ON_INDEX],CURSOR_POINTER_ON_IMAGE);
  pngLoad(&texturesArray[CURSOR_MOVE_INDEX],CURSOR_MOVE_IMAGE);
  pngLoad(&texturesArray[PLAYER_START_BUTTON_INDEX],PLAYER_START_BUTTON_IMAGE);
  pngLoad(&texturesArray[UI_SCROLLABLE_INDEX],UI_SCROLLABLE_IMAGE);
  pngLoad(&texturesArray[UI_SCROLL_PAD_INDEX],UI_SCROLL_PAD);
  pngLoad(&texturesArray[UI_TEXT_INPUT_INDEX],UI_TEXT_INPUT_IMAGE);
  pngLoad(&texturesArray[MEEPLE_INDEX],MEEPLE_IMAGE);
  pngLoad(&texturesArray[HEALTH_BAR_INDEX],HEALTH_BAR_IMAGE);
  pngLoad(&texturesArray[UNIT_BUILD_BAR_INDEX],UNIT_BUILD_BAR_IMAGE);
  pngLoad(&texturesArray[CITY_SANS_TREE_INDEX],CITY_SANS_TREE_IMAGE);
  pngLoad(&texturesArray[WALK_ICON_INDEX],WALK_ICON_IMAGE);
  pngLoad(&texturesArray[ADD_BUTTON_INDEX],ADD_BUTTON_IMAGE);
  pngLoad(&texturesArray[REMOVE_BUTTON_INDEX],REMOVE_BUTTON_IMAGE);
  pngLoad(&texturesArray[CITY_VIEWER_BOX_INDEX],CITY_VIEWER_BOX_IMAGE);
  pngLoad(&texturesArray[UNIT_TYPE_VIEWER_BOX_INDEX],UNIT_TYPE_VIEWER_BOX_IMAGE);
  pngLoad(&texturesArray[UNIT_VIEWER_BOX_INDEX],UNIT_VIEWER_BOX_IMAGE);
  pngLoad(&texturesArray[RESEARCH_BOX_INDEX],RESEARCH_BOX_IMAGE);
  pngLoad(&texturesArray[SELECTION_BRACKET_INDEX],SELECTION_BRACKET_IMAGE);
  pngLoad(&texturesArray[ADD_BUTTON_SMALL_INDEX],ADD_BUTTON_SMALL_IMAGE);
  pngLoad(&texturesArray[REMOVE_BUTTON_SMALL_INDEX],REMOVE_BUTTON_SMALL_IMAGE);
  pngLoad(&texturesArray[UNIT_CIRCLE_RED_INDEX],UNIT_CIRCLE_RED_IMAGE);
  pngLoad(&texturesArray[UNIT_CIRCLE_BLUE_INDEX],UNIT_CIRCLE_BLUE_IMAGE);
  pngLoad(&texturesArray[UNIT_CIRCLE_GREEN_INDEX],UNIT_CIRCLE_GREEN_IMAGE);
  pngLoad(&texturesArray[UNIT_CIRCLE_YELLOW_INDEX],UNIT_CIRCLE_YELLOW_IMAGE);
  pngLoad(&texturesArray[UNIT_CIRCLE_PINK_INDEX],UNIT_CIRCLE_PINK_IMAGE);
  pngLoad(&texturesArray[UNIT_CIRCLE_ORANGE_INDEX],UNIT_CIRCLE_ORANGE_IMAGE);
  pngLoad(&texturesArray[UNIT_CIRCLE_PURPLE_INDEX],UNIT_CIRCLE_PURPLE_IMAGE);
  pngLoad(&texturesArray[UNIT_CIRCLE_BROWN_INDEX],UNIT_CIRCLE_BROWN_IMAGE);
  pngLoad(&texturesArray[CURSOR_ATTACK_INDEX],CURSOR_ATTACK_IMAGE);
  pngLoad(&texturesArray[CURSOR_HEAL_INDEX],CURSOR_HEAL_IMAGE);
  pngLoad(&texturesArray[ARCHER_INDEX],ARCHER_IMAGE);
  pngLoad(&texturesArray[SWORDSMAN_INDEX],SWORDSMAN_IMAGE);
  pngLoad(&texturesArray[SELECTION_BOX_INDEX],SELECTION_BOX_IMAGE);
  pngLoad(&texturesArray[SUMMONER_INDEX],SUMMONER_IMAGE);
  pngLoad(&texturesArray[CITY_INDEX],CITY_IMAGE);
  pngLoad(&texturesArray[GATHERER_INDEX],GATHERER_IMAGE);
  pngLoad(&texturesArray[DRAGON_INDEX],DRAGON_IMAGE);
  pngLoad(&texturesArray[WHITE_MAGE_INDEX],WHITE_MAGE_IMAGE);
  pngLoad(&texturesArray[WOLF_INDEX],WOLF_IMAGE);
  pngLoad(&texturesArray[FIRE_INDEX],FIRE_IMAGE);
  pngLoad(&texturesArray[RED_MAGE_INDEX],RED_MAGE_IMAGE);
  pngLoad(&texturesArray[BLUE_MAGE_INDEX],BLUE_MAGE_IMAGE);
  pngLoad(&texturesArray[ICE_INDEX],ICE_IMAGE);
  pngLoad(&texturesArray[GAME_FIND_BACKGROUND_INDEX],GAME_FIND_BACKGROUND);
  pngLoad(&texturesArray[DEPRECATED_INDEX],DEPRECATED);
  pngLoad(&texturesArray[ROOMS_DISPLAY_INDEX],ROOMS_DISPLAY);
  pngLoad(&texturesArray[MODAL_INDEX],MODAL);
  pngLoad(&texturesArray[OK_BUTTON_INDEX],OK_BUTTON);
  pngLoad(&texturesArray[MODAL_BACKGROUND_INDEX],MODAL_BACKGROUND);
  pngLoad(&texturesArray[MODAL_SMALL_INDEX],MODAL_SMALL);
  pngLoad(&texturesArray[SEND_BUTTON_INDEX],SEND_BUTTON);
  pngLoad(&texturesArray[CHAT_BOX_INDEX],CHAT_BOX);
  pngLoad(&texturesArray[CHAT_DISPLAY_INDEX],CHAT_DISPLAY);
  pngLoad(&texturesArray[CREATE_GAME_BUTTON_INDEX],CREATE_GAME_BUTTON);
  pngLoad(&texturesArray[BACK_BUTTON_INDEX],BACK_BUTTON);
  pngLoad(&texturesArray[DA_1V1_BUTTON_INDEX],DA_1V1_BUTTON);
  pngLoad(&texturesArray[DA_2V2_BUTTON_INDEX],DA_2V2_BUTTON);
  pngLoad(&texturesArray[DA_3V3_BUTTON_INDEX],DA_3V3_BUTTON);
  pngLoad(&texturesArray[DA_4V4_BUTTON_INDEX],DA_4V4_BUTTON);
  pngLoad(&texturesArray[CREATE_GAME_BUTTON_LARGE_INDEX],CREATE_GAME_BUTTON_LARGE);
  pngLoad(&texturesArray[CREATE_GAME_BACKGROUND_LEFT_INDEX],CREATE_GAME_BACKGROUND_LEFT);
  pngLoad(&texturesArray[CREATE_GAME_BACKGROUND_RIGHT_INDEX],CREATE_GAME_BACKGROUND_RIGHT);
  pngLoad(&texturesArray[CREATE_GAME_BACKGROUND_TOP_INDEX],CREATE_GAME_BACKGROUND_TOP);
  pngLoad(&texturesArray[CREATE_GAME_BACKGROUND_BOTTOM_INDEX],CREATE_GAME_BACKGROUND_BOTTOM);
  pngLoad(&texturesArray[CREATE_GAME_BACKGROUND_INDEX],CREATE_GAME_BACKGROUND);
  pngLoad(&texturesArray[MAP_SELECTOR_INDEX],MAP_SELECTOR);
  pngLoad(&texturesArray[JOIN_GAME_BACKGROUND_INDEX],JOIN_GAME_BACKGROUND);
  pngLoad(&texturesArray[JOIN_GAME_CHAT_INDEX],JOIN_GAME_CHAT);
  pngLoad(&texturesArray[JOIN_GAME_CHAT_BOX_INDEX],JOIN_GAME_CHAT_BOX);
  pngLoad(&texturesArray[JOIN_GAME_PLAYERS_INDEX],JOIN_GAME_PLAYERS);
  pngLoad(&texturesArray[START_BUTTON_INDEX],START_BUTTON);
  pngLoad(&texturesArray[LOGIN_BUTTON_INDEX],LOGIN_BUTTON);
  pngLoad(&texturesArray[SCROLL_BAR_INDEX],SCROLL_BAR);
  pngLoad(&texturesArray[UNIT_UI_BACK_INDEX],UNIT_UI_BACK);
  pngLoad(&texturesArray[BUILD_BUTTON_INDEX],BUILD_BUTTON);
  pngLoad(&texturesArray[UI_CITY_BACKGROUND_INDEX],UI_CITY_BACKGROUND);
  pngLoad(&texturesArray[UI_UNIT_BACKGROUND_INDEX],UI_UNIT_BACKGROUND);
  pngLoad(&texturesArray[START_SUMMONING_BUTTON_INDEX],START_SUMMONING_BUTTON);
  pngLoad(&texturesArray[MOVE_BUTTON_INDEX],MOVE_BUTTON);
  pngLoad(&texturesArray[GREY_PEDESTAL_INDEX],GREY_PEDESTAL);
  pngLoad(&texturesArray[CANCEL_MOVEMENT_BUTTON_INDEX],CANCEL_MOVEMENT_BUTTON);
  pngLoad(&texturesArray[SKIP_BUTTON_INDEX],SKIP_BUTTON);
  pngLoad(&texturesArray[START_GATHERING_BUTTON_INDEX],START_GATHERING_BUTTON);
  pngLoad(&texturesArray[BUILD_BORDER_INDEX],BUILD_BORDER);
  pngLoad(&texturesArray[GREEN_WOOD_ICON_INDEX],GREEN_WOOD_ICON);
  pngLoad(&texturesArray[BLUE_WOOD_ICON_INDEX],BLUE_WOOD_ICON);
  pngLoad(&texturesArray[TIME_ICON_INDEX],TIME_ICON);
  pngLoad(&texturesArray[RESEARCH_BUTTON_INDEX],RESEARCH_BUTTON);
  pngLoad(&texturesArray[RESEARCH_BORDER_INDEX],RESEARCH_BORDER);
  pngLoad(&texturesArray[QUEUE_BORDER_INDEX],QUEUE_BORDER);
  pngLoad(&texturesArray[CANCEL_BUTTON_INDEX],CANCEL_BUTTON);
  pngLoad(&texturesArray[UI_UNITTYPE_BACKGROUND_INDEX],UI_UNITTYPE_BACKGROUND);
  pngLoad(&texturesArray[UI_CITYVIEW_BACKGROUND_INDEX],UI_CITYVIEW_BACKGROUND);
  pngLoad(&texturesArray[SLASH_ANIMATION_INDEX],SLASH_ANIMATION);
  pngLoad(&texturesArray[TITLE_INDEX],TITLE);
  pngLoad(&texturesArray[MENU_BUTTON_INDEX],MENU_BUTTON);
  pngLoad(&texturesArray[SWORDSMAN_OVERLAY_INDEX],SWORDSMAN_OVERLAY);
  pngLoad(&texturesArray[SUMMONER_OVERLAY_INDEX],SUMMONER_OVERLAY);
  pngLoad(&texturesArray[ARCHER_OVERLAY_INDEX],ARCHER_OVERLAY);
  pngLoad(&texturesArray[WHITE_MAGE_OVERLAY_INDEX],WHITE_MAGE_OVERLAY);
  pngLoad(&texturesArray[RED_MAGE_OVERLAY_INDEX],RED_MAGE_OVERLAY);
  pngLoad(&texturesArray[BLUE_MAGE_OVERLAY_INDEX],BLUE_MAGE_OVERLAY);
  pngLoad(&texturesArray[WOLF_OVERLAY_INDEX],WOLF_OVERLAY);
  pngLoad(&texturesArray[DRAGON_OVERLAY_INDEX],DRAGON_OVERLAY);
  pngLoad(&texturesArray[GATHERER_OVERLAY_INDEX],GATHERER_OVERLAY);
  pngLoad(&texturesArray[CONNECT_BUTTON_INDEX],CONNECT_BUTTON);
  pngLoad(&texturesArray[CHECK_MARK_INDEX],CHECK_MARK);
  pngLoad(&texturesArray[CHECK_MARK_CHECKED_INDEX],CHECK_MARK_CHECKED);
  pngLoad(&texturesArray[CHECKBOXES_BACKGROUND_INDEX],CHECKBOXES_BACKGROUND);
  pngLoad(&texturesArray[UI_CITY_EDITOR_BACKGROUND_BACKGROUND_INDEX],UI_CITY_EDITOR_BACKGROUND_BACKGROUND);
  pngLoad(&texturesArray[MENU_MODAL_INDEX],MENU_MODAL);
  pngLoad(&texturesArray[FOREST_INDEX0],FOREST0);
  pngLoad(&texturesArray[FOREST_INDEX1],FOREST1);
  pngLoad(&texturesArray[FOREST_INDEX2],FOREST2);
  pngLoad(&texturesArray[FOREST_INDEX3],FOREST3);
  pngLoad(&texturesArray[GRASS_INDEX0],GRASS0);
  pngLoad(&texturesArray[GRASS_INDEX1],GRASS1);
  pngLoad(&texturesArray[GRASS_INDEX2],GRASS2);
  pngLoad(&texturesArray[GRASS_INDEX3],GRASS3);
  pngLoad(&texturesArray[MOUNTAIN_INDEX0],MOUNTAIN0);
  pngLoad(&texturesArray[MOUNTAIN_INDEX1],MOUNTAIN1);
  pngLoad(&texturesArray[MOUNTAIN_INDEX2],MOUNTAIN2);
  pngLoad(&texturesArray[MOUNTAIN_INDEX3],MOUNTAIN3);
  pngLoad(&texturesArray[REDFOREST_INDEX0],REDFOREST0);
  pngLoad(&texturesArray[REDFOREST_INDEX1],REDFOREST1);
  pngLoad(&texturesArray[REDFOREST_INDEX2],REDFOREST2);
  pngLoad(&texturesArray[REDFOREST_INDEX3],REDFOREST3);
  pngLoad(&texturesArray[BLUEFOREST_INDEX0],BLUEFOREST0);
  pngLoad(&texturesArray[BLUEFOREST_INDEX1],BLUEFOREST1);
  pngLoad(&texturesArray[BLUEFOREST_INDEX2],BLUEFOREST2);
  pngLoad(&texturesArray[BLUEFOREST_INDEX3],BLUEFOREST3);
  pngLoad(&texturesArray[WATER_INDEX0],WATER0);
  pngLoad(&texturesArray[WATER_INDEX1],WATER1);
  pngLoad(&texturesArray[WATER_INDEX2],WATER2);
  pngLoad(&texturesArray[WATER_INDEX3],WATER3);

  vertexArrays[FOREST_TILE_INDEX] = *forestVertices;
  vertexArrays[GRASS_TILE_INDEX] = *grassVertices;
  vertexArrays[MOUNTAIN_TILE_INDEX] = *mountainVertices;
  vertexArrays[RED_FOREST_TILE_INDEX] = *forestVertices;
  vertexArrays[BLUE_FOREST_TILE_INDEX] = *blueForestVertices;
  vertexArrays[WATER_TILE_INDEX] = *waterVertices;
  vertexArrays[ROAD_TILE_INDEX] = *roadVertices;
  vertexArrays[CITY_TILE_INDEX] = *cityVertices;
  vertexArrays[PLAYER_START_TILE_INDEX] = *playerStartVertices;
  
  tilesLists = glGenLists(100);

  int c;
  int d;
  for(c=0;c<9;c++){
    for(d=0;d<4;d++){
      glNewList(tilesLists+(c*4)+d,GL_COMPILE);
      if(c <= 5){
	glBindTexture(GL_TEXTURE_2D, texturesArray[TILE_INDEX_START+(4*c)+d]);
	glBegin(GL_POLYGON);
	glTexCoord2f(textureHexVertices[0][0],textureHexVertices[0][1]); glVertex3f(hexagonVertices[0][0], hexagonVertices[0][1], 0.0);
	glTexCoord2f(textureHexVertices[1][0],textureHexVertices[1][1]); glVertex3f(hexagonVertices[1][0], hexagonVertices[1][1], 0.0);
	glTexCoord2f(textureHexVertices[2][0],textureHexVertices[2][1]); glVertex3f(hexagonVertices[2][0], hexagonVertices[2][1], 0.0);
	glTexCoord2f(textureHexVertices[3][0],textureHexVertices[3][1]); glVertex3f(hexagonVertices[3][0], hexagonVertices[3][1], 0.0);
	glTexCoord2f(textureHexVertices[4][0],textureHexVertices[4][1]); glVertex3f(hexagonVertices[4][0], hexagonVertices[4][1], 0.0);
	glTexCoord2f(textureHexVertices[5][0],textureHexVertices[5][1]); glVertex3f(hexagonVertices[5][0], hexagonVertices[5][1], 0.0);
	glEnd();
      }else{
	glBindTexture(GL_TEXTURE_2D, tilesTexture);
	glBegin(GL_POLYGON);
	glTexCoord2f(*(vertexArrays[c]+0),*(vertexArrays[c]+1)); glVertex3f(hexagonVertices[0][0], hexagonVertices[0][1], 0.0);
	glTexCoord2f(*(vertexArrays[c]+2),*(vertexArrays[c]+3)); glVertex3f(hexagonVertices[1][0], hexagonVertices[1][1], 0.0);
	glTexCoord2f(*(vertexArrays[c]+4),*(vertexArrays[c]+5)); glVertex3f(hexagonVertices[2][0], hexagonVertices[2][1], 0.0);
	glTexCoord2f(*(vertexArrays[c]+6),*(vertexArrays[c]+7)); glVertex3f(hexagonVertices[3][0], hexagonVertices[3][1], 0.0);
	glTexCoord2f(*(vertexArrays[c]+8),*(vertexArrays[c]+9)); glVertex3f(hexagonVertices[4][0], hexagonVertices[4][1], 0.0);
	glTexCoord2f(*(vertexArrays[c]+10),*(vertexArrays[c]+11)); glVertex3f(hexagonVertices[5][0], hexagonVertices[5][1], 0.0);
	glEnd();
      }
      glEndList();
    }
  }
  selectionBoxList = tilesLists+(c*d)+1;
  unitList = selectionBoxList+1;
  healthBarList = unitList+1;

  glNewList(selectionBoxList,GL_COMPILE);    
  glBegin(GL_QUADS);
  glTexCoord2f(0.0,0.0);
  glVertex3f(-0.88,-1.0,0.0);
  glTexCoord2f(1.0,0.0);
  glVertex3f(0.84,-1.0,0.0);
  glTexCoord2f(1.0,1.0);
  glVertex3f(0.84,1.0, 0.0);
  glTexCoord2f(0.0,1.0);
  glVertex3f(-0.88,1.0, 0.0);
  glEnd();
  glEndList();

  glNewList(unitList,GL_COMPILE);    
  glBegin(GL_QUADS);
  glTexCoord2f(0.0,0.0);
  glVertex3f(-0.75, -0.75, 0.0);
  glTexCoord2f(1.0,0.0);
  glVertex3f(0.75, -0.75, 0.0);
  glTexCoord2f(1.0,1.0);
  glVertex3f(0.75, 0.75, 0.0);
  glTexCoord2f(0.0,1.0);
  glVertex3f(-0.75, 0.75, 0.0);
  glEnd();
  glEndList();

  glNewList(healthBarList,GL_COMPILE);    
  glBegin(GL_QUADS);
  glTexCoord2f(0.0,0.0);
  glVertex3f(-.75, 1.05, -0.001);
  glTexCoord2f(1.0,0.0);
  glVertex3f(.75, 1.05, -0.001);
  glTexCoord2f(1.0,1.0);
  glVertex3f(.75, 0.85, -0.001);
  glTexCoord2f(0.0,1.0);
  glVertex3f(-.75, 0.85, -0.001);
  glEnd();
  glEndList();

}

static void initPython(){
  //http://docs.python.org/release/2.6.6/c-api/index.html
  //  char [100] = "-v";
  //	sprintf(path,"%s","hello");
  Py_SetPythonHome(".");
  Py_Initialize();
  char *pyArgv[1];
  pyArgv[0] = "";
  PySys_SetArgv(1, pyArgv);
  if(isWindows){
    PyObject* sys = PyImport_ImportModule("sys");
    PyObject* pystdout = PyFile_FromString("stdout.txt", "wt");
    if (-1 == PyObject_SetAttrString(sys, "stdout", pystdout)) {
      printf("NO STDOUT AVAILABLE");
    }
    PyObject* pystderr = PyFile_FromString("stderr.txt", "wt");
    if (-1 == PyObject_SetAttrString(sys, "stderr", pystderr)) {
      printf("NO STDERR AVAILABLE");
    }
    if(pystdout != NULL){
      Py_DECREF(pystdout);
    }
    if(pystderr != NULL){
      Py_DECREF(pystderr);
    }
    Py_DECREF(sys);
  }
}
SDL_Event event;
PyObject * pyFocusNextUnit;
char keyArray[20];
PyObject * pyClickScroll;
static void handleInput(){
  if(PyObject_HasAttrString(gameMode,"clickScroll")){
      pyClickScroll = PyObject_GetAttrString(gameMode, "clickScroll");//New reference
      clickScroll = pyClickScroll == Py_True;
      Py_DECREF(pyClickScroll);
  }
  if(PyObject_HasAttrString(gameMode,"getFocusNextUnit")){
    pyFocusNextUnit = PyObject_CallMethod(gameMode,"getFocusNextUnit",NULL);
    doFocus = PyLong_AsLong(pyFocusNextUnit);
    if(doFocus){
      isFocusing = 1;
    }
  }
  //SDL_Delay(20);//for framerate testing...

  if(keyHeld){
    if(repeatKey){
      if(SDL_GetTicks() - keyHeldTime > 40){
	keyHeldTime = SDL_GetTicks();

	       //	       || event.key.keysym.sym ==SDLK_RSHIFT
	       //	       || event.key.keysym.sym ==SDLK_LSHIFT


	if(PyObject_HasAttrString(gameMode,"handleKeyDown")){
	  pyObj = PyObject_CallMethod(gameMode,"handleKeyDown","s",keyArray);
	  printPyStackTrace();
	  Py_DECREF(pyObj);
	}
      }
    }else if(SDL_GetTicks() - keyHeldTime > 500){
      repeatKey = 1;
      keyHeldTime = SDL_GetTicks();
    }
  }
  while(SDL_PollEvent(&event)){
    switch(event.type){
    case SDL_MOUSEMOTION:
      mouseX = event.motion.x;
      mouseY = event.motion.y;
      if(PyObject_HasAttrString(gameMode,"handleMouseMovement")){
	pyObj = PyObject_CallMethod(gameMode,"handleMouseMovement","(iii)",selectedName,mouseX,mouseY);
	Py_DECREF(pyObj);
      }
      printPyStackTrace();
      if(mouseX == 0){
	moveRight = -1;
      }else if(mouseX >= SCREEN_WIDTH-1){
	moveRight = 1;
      }else{
	moveRight = 0;
      }
      if(mouseY == 0){
	moveUp = 1;
      }else if(mouseY >= SCREEN_HEIGHT-1){
	moveUp = -1;
      }else{
	moveUp = 0;
      }
      break;
    case SDL_MOUSEBUTTONDOWN:
      if(event.button.button == SDL_BUTTON_WHEELUP){
	if(PyObject_HasAttrString(gameMode,"handleScrollUp")){
	  pyObj = PyObject_CallMethod(gameMode,"handleScrollUp","i",selectedName);//New reference
	  Py_DECREF(pyObj);
	}
      }else if(event.button.button == SDL_BUTTON_WHEELDOWN){
	if(PyObject_HasAttrString(gameMode,"handleScrollDown")){
	  PyObject_CallMethod(gameMode,"handleScrollDown","i",selectedName);//New reference
	  Py_DECREF(pyObj);
	}
      }
      if(event.button.button == SDL_BUTTON_MIDDLE){
	//	clickScroll = 1;
      }
      if(event.button.button == SDL_BUTTON_LEFT){
	leftButtonDown = 1;
	if(PyObject_HasAttrString(gameMode,"handleLeftClickDown")){
	  pyObj = PyObject_CallMethod(gameMode,"handleLeftClickDown","i",selectedName);//New reference
	  printPyStackTrace();
	  Py_DECREF(pyObj);
	}
	previousClickedName = selectedName;
      }
      printPyStackTrace();
      if(event.button.button == SDL_BUTTON_RIGHT){
	//	clickScroll = 1;
	PyObject_CallMethod(gameMode,"handleRightClick","i",selectedName);//New reference
      }
      break;
    case SDL_MOUSEBUTTONUP:
      if(event.button.button == SDL_BUTTON_MIDDLE){
	//	clickScroll = 0;
      }
      if(event.button.button == SDL_BUTTON_LEFT){
	if(PyObject_HasAttrString(gameMode,"handleLeftClickUp")){
	  pyObj = PyObject_CallMethod(gameMode,"handleLeftClickUp","i",selectedName);//New reference
	  printPyStackTrace();
	  Py_DECREF(pyObj);
	}
	leftButtonDown = 0;
      }
      if(event.button.button == SDL_BUTTON_RIGHT){
	if(PyObject_HasAttrString(gameMode,"handleRightClickUp")){
	  pyObj = PyObject_CallMethod(gameMode,"handleRightClickUp","i",selectedName);//New reference
	  printPyStackTrace();
	  Py_DECREF(pyObj);
	}
      }
      break;
    case SDL_KEYDOWN:
      /*      if(event.key.keysym.sym == SDLK_ESCAPE){
	done = 1;	
	
      }else if(event.key.keysym.sym == SDLK_BACKQUOTE){
	clickScroll = 1;
	avgDeltaTicks = 0;
	totalDeltaTicksDataPoints = 0;
      }else */
      if(event.key.keysym.sym == SDLK_NUMLOCK
	       || event.key.keysym.sym ==SDLK_CAPSLOCK
	       || event.key.keysym.sym ==SDLK_SCROLLOCK
	       //	       || event.key.keysym.sym ==SDLK_RSHIFT
	       //	       || event.key.keysym.sym ==SDLK_LSHIFT
	       || event.key.keysym.sym ==SDLK_RCTRL
	       || event.key.keysym.sym ==SDLK_LCTRL
	       || event.key.keysym.sym ==SDLK_RALT
	       || event.key.keysym.sym ==SDLK_LALT
	       || event.key.keysym.sym == SDLK_RMETA
	       || event.key.keysym.sym == SDLK_LMETA
	       || event.key.keysym.sym == SDLK_LSUPER
	       || event.key.keysym.sym == SDLK_RSUPER
	       || event.key.keysym.sym == SDLK_MODE
	       || event.key.keysym.sym == SDLK_COMPOSE
	       || event.key.keysym.sym == SDLK_HELP
	       || event.key.keysym.sym == SDLK_PRINT
	       || event.key.keysym.sym == SDLK_SYSREQ
	       || event.key.keysym.sym == SDLK_BREAK
	       || event.key.keysym.sym == SDLK_MENU
	       || event.key.keysym.sym == SDLK_POWER
	       || event.key.keysym.sym == SDLK_EURO
	       || event.key.keysym.sym == SDLK_UNDO){
	printf("rejected: %d\n",event.key.keysym.sym);
      }else{
	if(event.key.keysym.sym != SDLK_RSHIFT && event.key.keysym.sym != SDLK_LSHIFT){
	  keyHeld = 1;
	  repeatKey = 0;
	}
	keyHeldTime = SDL_GetTicks();
	if((event.key.keysym.mod & KMOD_CAPS | event.key.keysym.mod & KMOD_LSHIFT | event.key.keysym.mod & KMOD_RSHIFT) && (event.key.keysym.sym > 0x60 && event.key.keysym.sym <= 0x7A)){
	  keyArray[0] = (*SDL_GetKeyName(event.key.keysym.sym))-32;
	  keyArray[1] = 0;
	}else if(event.key.keysym.mod & KMOD_LSHIFT | event.key.keysym.mod & KMOD_RSHIFT){
	  switch(event.key.keysym.sym){
	  case SDLK_COMMA:
	    keyArray[0] = SDLK_LESS;
	    keyArray[1] = 0;
	    break;
	  case SDLK_MINUS:
	    keyArray[0] = SDLK_UNDERSCORE;
	    keyArray[1] = 0;
	    break;
	  case SDLK_SEMICOLON:
	    keyArray[0] = SDLK_COLON;
	    keyArray[1] = 0;
	    break;
	  case SDLK_EQUALS:
	    keyArray[0] = SDLK_PLUS;
	    keyArray[1] = 0;
	    break;
	  case SDLK_PERIOD:
	    keyArray[0] = SDLK_GREATER;
	    keyArray[1] = 0;
	    break;
	  case SDLK_SLASH:
	    keyArray[0] = SDLK_QUESTION;
	    keyArray[1] = 0;
	    break;
	  case SDLK_LEFTBRACKET:
	    keyArray[0] = 123;
	    keyArray[1] = 0;
	    break;
	  case SDLK_RIGHTBRACKET:
	    keyArray[0] = 125;
	    keyArray[1] = 0;
	    break;
	  case SDLK_BACKSLASH:
	    keyArray[0] = 124;
	    keyArray[1] = 0;
	    break;
	  case SDLK_0:
	    keyArray[0] = SDLK_RIGHTPAREN;
	    keyArray[1] = 0;
	    break;
	  case SDLK_1:
	    keyArray[0] = SDLK_EXCLAIM;
	    keyArray[1] = 0;
	    break;
	  case SDLK_2:
	    keyArray[0] = SDLK_AT;
	    keyArray[1] = 0;
	    break;
	  case SDLK_3:
	    keyArray[0] = SDLK_HASH;
	    keyArray[1] = 0;
	    break;
	  case SDLK_4:
	    keyArray[0] = SDLK_DOLLAR;
	    keyArray[1] = 0;
	    break;
	  case SDLK_5:
	    keyArray[0] = 37;
	    keyArray[1] = 0;
	    break;
	  case SDLK_6:
	    keyArray[0] = SDLK_CARET;
	    keyArray[1] = 0;
	    break;
	  case SDLK_7:
	    keyArray[0] = SDLK_AMPERSAND;
	    keyArray[1] = 0;
	    break;
	  case SDLK_8:
	    keyArray[0] = SDLK_ASTERISK;
	    keyArray[1] = 0;
	    break;
	  case SDLK_9:
	    keyArray[0] = SDLK_LEFTPAREN;
	    keyArray[1] = 0;
	    break;
	  }
	}else{
	  sprintf(keyArray,"%s",SDL_GetKeyName(event.key.keysym.sym));
	}
	if(PyObject_HasAttrString(gameMode,"handleKeyDown")){	
	  pyObj = PyObject_CallMethod(gameMode,"handleKeyDown","s",keyArray); 
	  printPyStackTrace();
	  Py_DECREF(pyObj);
	}
      }
      break;
    case SDL_KEYUP:
      keyHeld = 0;
      repeatKey = 0;
      /*if(event.key.keysym.sym == SDLK_BACKQUOTE){
	clickScroll = 0;
	}else*/
      if(event.key.keysym.sym == 303//rightshift
	 || event.key.keysym.sym == 304//leftshift
	 || event.key.keysym.sym == SDLK_BACKQUOTE){
	if(PyObject_HasAttrString(gameMode,"handleKeyUp")){
	  pyObj = PyObject_CallMethod(gameMode,"handleKeyUp","s",SDL_GetKeyName(event.key.keysym.sym));
	  Py_DECREF(pyObj);
	}
      }
      break;
    case SDL_QUIT:
      done = 1;
      break;
    default:
      break;
    }
  }
}
PyObject * pyBackgroundImageIndex;
int backgroundImageIndex;
void drawBackground(){
  if(PyObject_HasAttrString(gameMode,"backgroundImageIndex")){
    pyBackgroundImageIndex = PyObject_GetAttrString(gameMode, "backgroundImageIndex");//New reference
    backgroundImageIndex = PyLong_AsLong(pyBackgroundImageIndex);
    glMatrixMode(GL_PROJECTION);
    glLoadIdentity();
    glMatrixMode(GL_MODELVIEW);
    glLoadIdentity();
    glBindTexture(GL_TEXTURE_2D, texturesArray[backgroundImageIndex]);
    glBegin(GL_QUADS);
    glTexCoord2f(0.0,0.0); glVertex3f(-1.0,-1.0,0.0);
    glTexCoord2f(1.0,0.0); glVertex3f(1.0,-1.0,0.0);
    glTexCoord2f(1.0,1.0); glVertex3f(1.0,1.0,0.0);
    glTexCoord2f(0.0,1.0); glVertex3f(-1.0,1.0,0.0);
    glEnd();
    Py_DECREF(pyBackgroundImageIndex);
  }
}
GLint viewport[4];
GLint hitsCnt;
PyObject * pyChooseNextDelayed;
int chooseNextDelayed;
Uint32 chooseNextTimeStart;
static void draw(){
  if(PyObject_HasAttrString(gameMode,"chooseNextDelayed")){
    pyChooseNextDelayed = PyObject_CallMethod(gameMode,"getChooseNextDelayed",NULL);//New reference
    printPyStackTrace();
    Py_DECREF(pyChooseNextDelayed);
    if(pyChooseNextDelayed == Py_True){
      chooseNextTimeStart = SDL_GetTicks();
      chooseNextDelayed = 1;
    }
  }
  if(chooseNextDelayed && ((SDL_GetTicks() - chooseNextTimeStart) > AUTO_CHOOSE_NEXT_DELAY)){
    chooseNextDelayed = 0;
    pyObj = PyObject_CallMethod(gameMode,"sendChooseNextUnit",NULL);//New reference
    printPyStackTrace();
    Py_DECREF(pyObj);
  }
  PyObject_SetAttrString(gameMode,"ticks",PyLong_FromLong(SDL_GetTicks()));
  if(PyObject_HasAttrString(gameMode,"onDraw")){
    pyObj = PyObject_CallMethod(gameMode,"onDraw","i",deltaTicks);//New reference
    printPyStackTrace();
    Py_DECREF(pyObj);
  }

  glClear(GL_COLOR_BUFFER_BIT | GL_DEPTH_BUFFER_BIT);		 
  glSelectBuffer(BUFSIZE,selectBuf);//glSelectBuffer must be issued before selection mode is enabled, and it must not be issued while the rendering mode is GL_SELECT.

  doViewport();
  theCursorIndex = -1;
  glGetIntegerv(GL_VIEWPORT,viewport);
  glMatrixMode(GL_PROJECTION);
  glLoadIdentity();
  gluPickMatrix(mouseX,SCREEN_HEIGHT-mouseY,1,1,viewport);
  gluPerspective(45.0f,(float)viewport[2]/(float)viewport[3],minZoom,maxZoom);
  glMatrixMode(GL_MODELVIEW);
  glLoadIdentity();
  glTranslatef(translateX,translateY,translateZ);
  glRenderMode(GL_SELECT);
  drawBoard();

  glMatrixMode(GL_PROJECTION);
  glLoadIdentity();
  glViewport(0, 0, SCREEN_WIDTH, SCREEN_HEIGHT);
  glGetIntegerv(GL_VIEWPORT,viewport);
  gluPickMatrix(mouseX,SCREEN_HEIGHT-mouseY,1,1,viewport);
  glMatrixMode(GL_MODELVIEW);
  glLoadIdentity();
  drawUI();

  hitsCnt = glRenderMode(GL_RENDER);
  processTheHits(hitsCnt,selectBuf);

  glMatrixMode(GL_PROJECTION);
  glLoadIdentity();
  glGetIntegerv(GL_VIEWPORT,viewport);
  gluPerspective(45.0f,(float)viewport[2]/(float)viewport[3],minZoom,maxZoom);
  glMatrixMode(GL_MODELVIEW);
  glLoadIdentity();
  calculateTranslation();

  glClear(GL_COLOR_BUFFER_BIT | GL_DEPTH_BUFFER_BIT);		

  drawBackground();

  doViewport();
  glMatrixMode(GL_PROJECTION);
  glLoadIdentity();
  glGetIntegerv(GL_VIEWPORT,viewport);
  gluPerspective(45.0f,(float)viewport[2]/(float)viewport[3],minZoom,maxZoom);
  glMatrixMode(GL_MODELVIEW);

  glLoadIdentity();
  glColor3f(0.0,0.0,0.0);
  glBegin(GL_QUADS);
  glTexCoord2f(0.0,0.0); glVertex3f(-1.0,-1.0,-1.01);
  glTexCoord2f(1.0,0.0); glVertex3f(1.0,-1.0,-1.01);
  glTexCoord2f(1.0,1.0); glVertex3f(1.0,1.0,-1.01);
  glTexCoord2f(0.0,1.0); glVertex3f(-1.0,1.0,-1.01);
  glEnd();
  
  glTranslatef(translateX,translateY,translateZ);
  glDepthFunc(GL_GEQUAL);
  drawBoard();
  glDepthFunc(GL_ALWAYS);

  glMatrixMode(GL_PROJECTION);
  glLoadIdentity();
  glMatrixMode(GL_MODELVIEW);
  glLoadIdentity();
  glViewport(0, 0, SCREEN_WIDTH, SCREEN_HEIGHT);
  drawUI();

  glFlush();
  SDL_GL_SwapBuffers ();	
}
PyObject * pyExit;
static void mainLoop (){
  while ( !done ) {
    gameMode = PyObject_CallMethod(gameState,"getGameMode",NULL);
    if(PyObject_HasAttrString(gameMode,"map")){
      theMap = PyObject_GetAttrString(gameMode, "map");//New reference
    }
    pyExit = PyObject_GetAttrString(gameMode,"exit");
    done = (pyExit == Py_True);
    deltaTicks = SDL_GetTicks()-currentTick;
    currentTick = SDL_GetTicks();
    handleInput();
    draw();
    if(PyObject_HasAttrString(gameMode,"map")){
      Py_DECREF(theMap);
    }
    Py_DECREF(gameMode);
  }
  pyObj = PyObject_CallMethod(gameMode,"onQuit",NULL);
  Py_DECREF(pyObj);
}
int nextPowerOf2(unsigned int v){
  const unsigned int b[] = {0x2, 0xC, 0xF0, 0xFF00, 0xFFFF0000};
  const unsigned int S[] = {1, 2, 4, 8, 16};
  int i;
  register unsigned int r = 0; // result of log2(v) will go here
  for (i = 4; i >= 0; i--){ // unroll for speed...
    if (v & b[i]){
      v >>= S[i];
      r |= S[i];
    } 
  }
  return pow(2,r+1);
}

int main(int argc, char **argv){
  if ( SDL_Init (SDL_INIT_VIDEO) < 0 ) {
    fprintf(stderr, "Couldn't initialize SDL: %s\n",SDL_GetError());
    exit(1);
  }
  SDL_GL_SetAttribute (SDL_GL_DEPTH_SIZE, 16);
  //  SDL_GL_SetAttribute (SDL_GL_DOUBLEBUFFER, 1);
  Uint32 flags = SDL_OPENGL;
  if(FULL_SCREEN){
    flags |= SDL_FULLSCREEN;
  }
  gScreen = SDL_SetVideoMode (SCREEN_WIDTH, SCREEN_HEIGHT, 0, flags);
  if (gScreen == NULL) {
    fprintf (stderr, "Could not set OpenGL video mode: %s\n",
	     SDL_GetError());
    SDL_Quit();
    exit(2);
  }
  int * value;
  //  SDL_GL_GetAttribute(SDL_GL_DEPTH_SIZE,value);
  //  printf("depth size: %d\n",*value);
  SDL_ShowCursor(0);
  initGL();
  const GLubyte * glVersion = glGetString(GL_VERSION);
  //  printf("OpenGL Version: %s\n",glVersion);
  initPython();
  initFonts();
  //SDL_EnableUNICODE(1);
  gameModule = PyImport_ImportModule("gameModes");//New reference
  gameState = PyImport_ImportModule("gameState");
  mainLoop();
  Py_DECREF(gameModule);
  Py_DECREF(gameState);
  Py_Finalize();
  exit(0);
}
