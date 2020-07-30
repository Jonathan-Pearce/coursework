im = imread('james.jpg'); %read image
im_grey = im(:,:,2); %green channel
im_double = im2double(im_grey);

%create gaussian pyramid
level1 = imgaussfilt(im_double,1);
level2 = imresize(imgaussfilt(im_double,2),1/2.0);
level3 = imresize(imgaussfilt(im_double,4),1/4.0);
level4 = imresize(imgaussfilt(im_double,8),1/8.0);
level5 = imresize(imgaussfilt(im_double,16),1/16.0);
level6 = imresize(imgaussfilt(im_double,32),1/32.0);
gaussImages = {level1,level2,level3,level4,level5,level6};

% % create composite image of gaussian pyramid
% % https://stackoverflow.com/questions/27002563/display-a-gaussian-pyramid-stored-in-a-cell-array-in-a-single-figure

% border=5;
% MergedImage=ones(size(gaussImages{1},1), 2.5*size(gaussImages{1},2));
% MergedImage(1:size(gaussImages{1},1), 1:size(gaussImages{1},2))=gaussImages{1};
% Pos=[1, size(gaussImages{1},1)+border];
% for k=1:(numel(gaussImages)-1)
%     MergedImage(Pos(1):Pos(1)+size(gaussImages{k+1}, 1)-1, Pos(2):Pos(2)+size(gaussImages{k+1}, 2)-1)=gaussImages{k+1};
%     Pos=[Pos(1), Pos(2)+size(gaussImages{k+1}, 2)+border];
% end
% imshow(MergedImage);
% imwrite(MergedImage,'gaussPyr.jpg')
% %%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%
% 

% create Laplacian pyramid
lapLevel1 = (level1 - imresize(level2,2));
lapLevel2 = (level2 - imresize(level3,2));
lapLevel3 = (level3 - imresize(level4,2));
lapLevel4 = (level4 - imresize(level5,2));
lapLevel5 = (level5 - imresize(level6,2));
lapLevel6 = level6;
laplacImages = {lapLevel1,lapLevel2,lapLevel3,lapLevel4,lapLevel5,lapLevel6};

% % create composite image of laplacian pyramid
% % https://stackoverflow.com/questions/27002563/display-a-gaussian-pyramid-stored-in-a-cell-array-in-a-single-figure

% border=5;
% MergedLapImage=ones(size(laplacImages{1},1), 2.5*size(laplacImages{1},2));
% MergedLapImage(1:size(laplacImages{1},1), 1:size(laplacImages{1},2))=laplacImages{1};
% Pos=[1, size(laplacImages{1},1)+border];
% for k=1:(numel(laplacImages)-1)
%     MergedLapImage(Pos(1):Pos(1)+size(laplacImages{k+1}, 1)-1, Pos(2):Pos(2)+size(laplacImages{k+1}, 2)-1)=laplacImages{k+1};
%     Pos=[Pos(1), Pos(2)+size(laplacImages{k+1}, 2)+border];
% end
% imshow(MergedLapImage);
% imwrite(10*MergedLapImage,'lapPyr_10.jpg')


%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%
%SIFT Keypoint location

%vectors that contain keypoint info (x,y,sigma)
keypoint_x_total = [];
keypoint_y_total = [];
keypoint_scale_total = [];

%helpers to make circles of different scale (sizes) different colours
colour = [];
colors = {'r','g','b','y'};

%show image
imshow(im_double)

%Threshold to help remove low quality keypoints
delta = 0.002;

%Iterate through levels of laplacian pyramid
%NOTE: don't look through edges levels since you cannot upsample or
%downsample an image to compare with
for n = 1:4
    keypoint_x = [];
    keypoint_y = [];
    keypoint_scale = [];
    %get image at level of laplacian pyramid
    curImage = laplacImages{n+1};
    %get image from upper level, and upsample to match dimensions
    upSampleImage = imresize(laplacImages{n+2},2);
    %get image from lower level and downsample to match dimensions
    downSampleImage = imresize(laplacImages{n},1/2.0);


    %iterate through current image
    for a = 1:size(curImage,1)-2
        for b = 1:size(curImage,2)-2
            %matrix of zeroes that will represent neighbourhood of
            %candidate point
            M = zeros([3 3 3]); 
            %populate neighbourhood with intensity values
            for c = 0:2
                for d = 0:2
                    M(c+1,d+1,1) = downSampleImage(a+c,b+d);
                    M(c+1,d+1,2) = curImage(a+c,b+d);
                    M(c+1,d+1,3) = upSampleImage(a+c,b+d);
                end
            end

            %maximum value and index of maximum in neighbourhood
            [C,I_max] = max(M(:));
            I_max;
            C;
            
            %minimum value and index of minimum in neighbourhood
            [D,I_min] = min(M(:));
            I_min;
            D;
            
            %If the candidate point is a maximum we may have found a
            %keypoint
            if I_max == 14
                %replace candidate point value with a different value
                M(2,2,2) = M(1,1,1);
                %get new maximum, i.e. second maximum of original matrix
                C_new = max(M(:));
                %check whether first and second maximum are different
                %enough
                %if yes, then candidate point is a significant keypoint
                if abs(C-C_new) > delta
                    %add candidate point data to keypoint vectors
                    %mulitply pixel values by 2^n and correct by shifting
                    %it back 2^(n-1) (i.e. half of scale pixel)
                    %this brings keypoint location error down to 2^(n-1)
                    keypoint_y = [keypoint_y,(a+1)*(2^n) - (2^n)/2];
                    keypoint_x = [keypoint_x,(b+1)*(2^n) - (2^n)/2];
                    keypoint_scale = [keypoint_scale,2^n];
                    %colour = [colour,colors{n}];
                end
            elseif I_min == 14
                %replace candidate point value with a different value
                M(2,2,2) = M(1,1,1);
                %get new minimum, i.e. second minimum of original matrix
                D_new = min(M(:));
                %check whether first and second minimum are different
                %enough
                %if yes, then candidate point is a significant keypoint
                if abs(D-D_new) > delta
                    %add candidate point data to keypoint vectors
                    %mulitply pixel values by 2^n and correct by shifting
                    %it back 2^(n-1) (i.e. half of scale pixel)
                    %this brings keypoint location error down to 2^(n-1)
                    keypoint_y = [keypoint_y,(a+1)*(2^n) - (2^n)/2];
                    keypoint_x = [keypoint_x,(b+1)*(2^n) - (2^n)/2];
                    keypoint_scale = [keypoint_scale,2^n];
                    %colour = [colour,colors{n}];
                end
            end

        end
    end

    %update total keypoint vectors
    %necessary to make different circles different colours
    keypoint_x_total = [keypoint_x_total, keypoint_x];
    keypoint_y_total = [keypoint_y_total, keypoint_y];
    keypoint_scale_total = [keypoint_scale_total, keypoint_scale];
    
    %transform keypoint data for plotting keypoint circles
    centers = [transpose(keypoint_x) transpose(keypoint_y)];
    radii = transpose(keypoint_scale);
    fin_colours = transpose(colour);
    %plot keypoint circles on image
    viscircles(centers,radii,'LineWidth',0.5,'Color',colors{n});

    
end


%Code for part 3
if 3 == 4
    
    k = 1.05;
    sigma = 3;
    windowSize = 25;

    %LOG code
    h = (k-1)*sigma*sigma*fspecial('log',windowSize,sigma);
    %surf(h)
    %contourf(h)
    %title('Laplacian of Gaussian')

    %DOG code
    g = fspecial('gaussian',windowSize,k*sigma) -  fspecial('gaussian',windowSize,sigma);
    %surf(g)
    %contourf(g)
    %title('Difference of Gaussians')

end
