typedef struct unit{
  float xPos, yPos, health, maxHealth;
  char textureIndex;
}UNIT;
typedef struct node{
  //  UNIT * unit;
  long name;
  float xPos;
  float yPos;
  char xIndex;
  char yIndex;
  char tileValue;
  //  char pyRoadValue;
  //  char city;
  char playerStartValue;
  //  char selected;
  char onMovePath;
  //  char cursorIndex;
  char visible;
}NODE;

typedef struct map{
  struct node * nodes;
  int polarity;
  int height;
  int width;
  int size;
} MAP;
