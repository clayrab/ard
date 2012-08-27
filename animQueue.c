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
