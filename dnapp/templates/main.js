function imageCoordsFromClickEvent(event) {
  pxX = event.x - event.offsetLeft;
  pxY = event.layerY;
  cH = event.srcElement.clientHeight;
  nH = event.srcElement.naturalHeight;
  cScale = cH / nH;
  rX = pxX / cScale;
  rY = pxY / cScale;
  return { 'img_x': rX, 'img_y': rY, 'scale': cScale }
}