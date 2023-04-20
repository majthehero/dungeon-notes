function imageCoordsFromClickEvent(event) {
  pxX = event.x - event.target.offsetLeft;
  pxY = event.layerY;
  cH = event.srcElement.clientHeight;
  nH = event.srcElement.naturalHeight;
  cScale = cH / nH;
  rX = pxX / cScale;
  rY = pxY / cScale;
  return { 'rX': rX, 'rY': rY }
}