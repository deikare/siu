clear;

dimmensions = [1920 1080];
mToPx = 22;
gap = 4;
borderDimmensions = dimmensions - 2 * gap * mToPx; % times 2, because of gaps from each side
borderPositions = [(mToPx * gap) (dimmensions(1) - mToPx * gap); (mToPx * gap) (dimmensions(2) - mToPx * gap)];

gimpCoordinates = [271 894; 
    201 860;
    185 778;
    186 671;
    221 565;
    431 393;
    1506 415;
    1591 369;
    1594 284;
    1496 187;
    1256 176;
    1140 227;
    1057 282;
    1034 521;
    1131 630;
    1354 701;
    1446 763;
    1458 842;
    1348 893];

gimpCoordinatesTransformed = [gimpCoordinates(:, 1), (dimmensions(2) - gimpCoordinates(:, 2))]

getDirections(gimpCoordinatesTransformed(1, :), gimpCoordinatesTransformed(2, :), 1)

function directions = getDirections(beg, finish, velocity)
    % velocity from 0 to 1
    delta = 50;
    translation = 200;

    directionsRaw = finish - beg;
    
    vectorLength = sqrt(directionsRaw(1)^2 + directionsRaw(2)^2);
    directions = translation + velocity * delta * directionsRaw / vectorLength;
end