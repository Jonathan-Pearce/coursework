im = imread('james_edges.png'); %read Binary edge image
im_double = im2double(im);

%These will be vectors that contain the x and y coordinates of the inliers
%in the best edge
x_final = 0;
y_final = 0;
%number of inliers in best model
max_inliers = 0;

%RANSAC Algorithm
%Run for T iterations
for T = 1:250
    %get random index
    index = randi(size(col,1));

    %get x,y and angle of that index
    y_0 = row(index,1);
    x_0 = col(index,1);
    theta_0 = ori(index,1);

    %I may have messed up my axis in my implmentation
    %In theory I should have to add pi/2 to get the angle along the edge
    %that a gradient is representing, since gradients are perpendicular to
    %the edge
    %I started with pi/2 and my algorithm did not work, but with removing
    %the pi/2 my code works, so I must have flipped an axis somewhere and
    %it compensated for this pi/2 computation
    
    %Line model calculations
    %Line model is of the form xcos(theta) + ysin(theta) = r
    theta = theta_0;
    %calculate r for corresponding angle and sampled point
    r = cos(theta)*x_0 + sin(theta)*y_0;

    inliers = 0;
    x = [];
    y = [];
    %iterate through every edge point
    for a = 1:size(col,1)
       %skip the proposal point
       if a ~= index
           %get x,y and angle of edge point
           y_i = row(a,1);
           x_i = col(a,1);
           theta_i = ori(a,1);

           %calculate distance from line model
           dist = abs(x_i * cos(theta) + y_i * sin(theta) - r);
                      
           %distance and angle comparison
           %these two conditions must be met in order for an edge point to
           %be an inlier for our edge model
           if dist < 3 && abs(theta_0 - theta_i) < pi/8
               %increase count of inliers
               inliers = inliers + 1;
               %save x and y value of edge point
               x = [x,x_i];
               y = [y,y_i];
           end
       end
       
    end
    
    %if current Line model had more inliers than current best line model,
    %then we have a new best line model
    if inliers > max_inliers
        %update data for best line model
        x_final = x;
        y_final = y;
        max_inliers = inliers;
    end
end


%creating image of edge points
%inliers of best line model will be red ([255,0,0])
%outliers of best line model will be black ([0,0,0])
test = 255 * ones(512, 512, 3, 'uint8');
x_final = transpose(x_final);
y_final = transpose(y_final);

%set all edge points to black
for a = 1:size(col)
  test(row(a), col(a), 1) = 0;
  test(row(a), col(a), 2) = 0;
  test(row(a), col(a), 3) = 0;
end
%chnage inliers to red
for a = 1:size(x_final,1)
  test(y_final(a), x_final(a), 1) = 255;
  test(y_final(a), x_final(a), 2) = 0;
  test(y_final(a), x_final(a), 3) = 0;
end

%display image
imshow(test)
imwrite(test,'q3Line.jpg')

