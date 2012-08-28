typedef struct uiElement{
  struct uiElement * nextElement;  
  struct uiElement * childElements;
  long name;
  float xPosition,yPosition,width,height,textSize,textXPosition,textYPosition;
  int textureIndex,cursorPosition;
  char hidden,cursorIndex,fontIndex,focused;
  char * text;
  char * textColor;
  char * color;
  char * mouseOverColor;
}UIELEMENT;
typedef struct unit{
  char * id;
  struct unit * nextUnit;
  double xPos,yPos,xPosDraw,yPosDraw;
  long health,maxHealth;
  char textureIndex,isNextUnit;
}UNIT;
typedef struct node{
  //  UNIT * unit;
  long name;
  uint hash;
  float xPos;
  float yPos;
  char xIndex;
  char yIndex;
  char tileValue;
  //  char pyRoadValue;
  //  char city;
  char playerStartValue;
  //  char selected;
  //  char onMovePath;
  //  char cursorIndex;
  char visible;
}NODE;
typedef struct map{
  struct node * nodes;
  int polarity;
  int height;
  int width;
  int size;
}MAP;
