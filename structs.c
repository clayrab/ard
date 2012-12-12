typedef struct pythonCallback{
  struct pythonCallback * nextCallback;
  int id, selectedName, mouseX, mouseY, leftButtonDown, deltaTicks, isAnimating, leftmostCharPos, rightmostCharPos, nameValue;
  char keyArray[200];
}PYTHONCALLBACK;
typedef struct uiElementStruct{
  struct uiElementStruct * nextElement;  
  struct uiElementStruct * childElements;
  int name;
  float xPosition,yPosition,width,height,textSize,textXPosition,textYPosition;
  int textureIndex,cursorPosition,leftmostCharPos,rightmostCharPos;
  char hidden,cursorIndex,fontIndex,focused, recalculateText;
  char * realText;
  char * text;
  char * textColor;
  char * color;
  char * mouseOverColor;
}UIELEMENTSTRUCT;
typedef struct unit{
  char * id;
  struct unit * nextUnit;
  double xPos,yPos,xPosDraw,yPosDraw;
  int health,maxHealth;
  char textureIndex,isNextUnit;
}UNIT;
typedef struct node{
  //  UNIT * unit;
  int name;
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
typedef struct cityNodeListElem{
  struct cityNodeListElem * nextCity;
  NODE * node;
}CITYNODELISTELEM;
typedef struct map{
  struct node * nodes;
  int polarity;
  int height;
  int width;
  int size;
}MAP;
typedef struct movePathNode{
  struct movePathNode * nextNode;
  float xPos;
  float yPos;
}MOVEPATHNODE;
typedef struct selectedNode{
  float xPos;
  float yPos;
}SELECTEDNODE;
typedef struct sound{
  struct sound * nextSound;
  int index;
}SOUND;
typedef struct animation{
  Uint32 time;
  int type;
  float xPos, yPos;
  long damage;
  struct unit * unit;
}ANIMATION;
//typedef struct animation animation;
struct listelement{
  ANIMATION * item;
  struct listelement * link;
};
typedef struct listelement listelement;

listelement * AddItem(listelement * listpointer, ANIMATION * animation){
  listelement * lp = listpointer;
  if(listpointer != 0) {
    while(listpointer->link != 0)
      listpointer = listpointer->link;
    listpointer->link = (struct listelement *)malloc(sizeof(listelement));
    listpointer = listpointer->link;
    listpointer->link = 0;
    listpointer->item = animation;
    return lp;
  }
  else {
    listpointer = (struct listelement *)malloc(sizeof(listelement));
    listpointer->link = 0;
    listpointer->item = animation;
    return listpointer;
  }
}

listelement * RemoveItem(listelement * listpointer) {
  listelement * tempp;
  //  printf("Element removed is %d\n", listpointer->item);
  tempp = listpointer->link;
  free(listpointer);
  return tempp;
}
