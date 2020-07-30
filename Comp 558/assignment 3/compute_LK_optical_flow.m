function [Vx,Vy] = compute_LK_optical_flow(frame_1,frame_2,type_LK)

% You have to implement the Lucas Kanade algorithm to compute the
% frame to frame motion field estimates. 
% frame_1 and frame_2 are two gray frames where you are given as inputs to 
% this function and you are required to compute the motion field (Vx,Vy)
% based upon them.
% -----------------------------------------------------------------------%
% YOU MUST SUBMIT ORIGINAL WORK! Any suspected cases of plagiarism or 
% cheating will be reported to the office of the Dean.  
% You CAN NOT use packages that are publicly available on the WEB.
% -----------------------------------------------------------------------%

% There are three variations of LK that you have to implement,
% select the desired alogrithm by passing in the argument as follows:
% "LK_naive", "LK_iterative" or "LK_pyramid"



frame_1_blur = frame_1;
frame_2_blur = frame_2;
%we will only smooth the images when they are initially passed through
if size(frame_1,3)==3
    %need a gray scale image
    frame_1 = rgb2gray(frame_1);
    frame_2 = rgb2gray(frame_2);
    
    %change to double data type
    frame_1 = im2double(frame_1);
    frame_2 = im2double(frame_2);
    
    %blur images (only slightly to try and preserve edge and corner
    %features)
    frame_1_blur = imgaussfilt(frame_1,0.25);
    frame_2_blur = imgaussfilt(frame_2,0.25);
    
end

%get size of image
[height, width] = size(frame_1);

switch type_LK

    case "LK_naive"        
        %window size - parameter
        windowSize = 31;
            
        %half size of window, to help with indexing and padding
        m = floor(windowSize/2);
        %imshow(frame_1_blur)
        
        %pad image border with zeroes
        frame_1_pad = padarray(frame_1_blur, [m m],0, 'both');
        frame_2_pad = padarray(frame_2_blur, [m m],0, 'both');

        %define our velocity matrices (same size as input images)
        Vx = zeros(height,width);
        Vy = zeros(height,width);

        %gradient of I^n
        [dx,dy] = gradient(frame_1_pad);
        
        %create gaussian weighting matrix
        W = fspecial('gaussian',windowSize,10);
        
        %calculate image differences
        image_Diff = frame_1_pad - frame_2_pad;
        
        %precompute derivate and image difference calculations to help with
        %memory efficiency
        dx_2 = dx.*dx;
        dx_dy = dx.*dy;
        dy_2 = dy.*dy;
        diff_dx = image_Diff.*dx;
        diff_dy = image_Diff.*dy;
        
        %iterate over image
        for y = (m+1):(size(frame_1_pad,1)-m)
            for x = (m+1):(size(frame_1_pad,2)-m)
                
                %get second moment matrix values for the neighbourhood
                dx2_window = dx_2(y-m:y+m,x-m:x+m);
                dxdy_window = dx_dy(y-m:y+m,x-m:x+m);
                dy2_window = dy_2(y-m:y+m,x-m:x+m);

                %left side of equation calculation
                %element wise multiplication with gaussian weight matrix
                ATA_11 = W.*(dx2_window);
                ATA_12 = W.*(dxdy_window);
                ATA_21 = W.*(dxdy_window);
                ATA_22 = W.*(dy2_window);  

                %create 2x2 matrix
                ATA = [sum(ATA_11(:)) sum(ATA_12(:)); sum(ATA_21(:)) sum(ATA_22(:))];
                %%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%
                %Right hand side of equation

                %get values for the neighbourhood
                diff_window_x = diff_dx(y-m:y+m,x-m:x+m); 
                diff_window_y = diff_dy(y-m:y+m,x-m:x+m); 
                
                %right side of equation calculation
                %element wise multiplication with gaussian weight matrix
                B_1 = W.*(diff_window_x);
                B_2 = W.*(diff_window_y);
                
                %create matrix
                B = [-sum(B_1(:)); -sum(B_2(:))]; 

                %ensure second moment matrix is not singular
                if abs(det(ATA)) > 1e-40
                    %solve for Vx and Vy
                    v = ATA\B;
                    Vx(y-m,x-m) = -v(1);
                    Vy(y-m,x-m) = -v(2); 
                else
                    v = 0;
                    det(ATA)
                    Vx(y-m,x-m) = 0;
                    Vy(y-m,x-m) = 0; 
                end
            end 
        end
        %z = 4

    case "LK_iterative"
        %iterative velocity matrices
        Vx_k = zeros(height,width);
        Vy_k = zeros(height,width);
        
        %compute initial vectors
        [Vx,Vy] = compute_LK_optical_flow(frame_1_blur,frame_2_blur,"LK_naive");
        
        %was unable to find efficient convergence so I just capped my
        %program at 5 iterations
        %takes ~20-30 seconds
        for k = 1:5
            mean2(abs(Vx));
            mean2(abs(Vy));
            
            %update iterative velocity vector
            Vx_k = Vx_k + Vx;
            Vy_k = Vy_k + Vy;

            %warped I^n
            frame_1_k = zeros(height,width);

            %compute cell values for warped I^n
            for i = 1:height
                for j = 1:width
                    
                    %make sure we stay within image
                    y_new = round(i + Vy_k(i,j),0);
                    if y_new < 1
                        y_new = 1;
                    end
                    if y_new > height
                        y_new = height;
                    end
                    
                    x_new = round(j + Vx_k(i,j),0);
                    if x_new < 1
                        x_new = 1;
                    end
                    if x_new > width
                        x_new = width;
                    end
                    
                    frame_1_k(i,j) = frame_1(y_new,x_new); 
                end
            end
            
            %solve for Vx and Vy with I^k(x,y) (warped I^n) 
            [Vx,Vy] = compute_LK_optical_flow(frame_1_k,frame_2,"LK_naive");
        end
        %ensure we return the correct values
        Vx = Vx_k;
        Vy = Vy_k;

    case "LK_pyramid"        
        %I pyramid
        I1 = frame_1_blur;
        I2 = impyramid(I1, 'reduce');
        I3 = impyramid(I2, 'reduce');
        %J pyramid
        J1 = frame_2_blur;
        J2 = impyramid(J1, 'reduce');
        J3 = impyramid(J2, 'reduce');
        
        I_pyr = {I1,I2,I3};
        J_pyr = {J1,J2,J3};
        
        %estimate motion field at coarsest scale
        [Vx_k,Vy_k] = compute_LK_optical_flow(I_pyr{3},J_pyr{3},"LK_iterative");
        
        %iterate through other pyramid levels
        for k = 1:2
            %rescale motion fields to next level in pyramid and multiply by 
            %2 to scale vectors to correct size
            Vx_k_scaled = 2*(imresize(Vx_k,2));
            Vy_k_scaled = 2*(imresize(Vy_k,2));

            %get size of next pyramid level
            [level_height, level_width] = size(I_pyr{3-k});
            
            %warped I^k+1
            I_k_star = zeros(level_height,level_width);

            %compute cell values for warped I^k+1
            for i = 1:level_height
                for j = 1:level_width

                    y_new = round(i + Vy_k_scaled(i,j),0);
                    if y_new < 1
                        y_new = 1;
                    end
                    if y_new > level_height
                        y_new = level_height;
                    end

                    x_new = round(j + Vx_k_scaled(i,j),0);
                    if x_new < 1
                        x_new = 1;
                    end
                    if x_new > level_width
                        x_new = level_width;
                    end

                    %calculate warped pixel location
                    I_k_star(i,j) = I_pyr{3-k}(y_new,x_new); 
                end
            end

            %iterativly compute new motion field with warped I^k+1
            [Vx_k,Vy_k] = compute_LK_optical_flow(I_k_star,J_pyr{3-k},"LK_iterative");
        end
        %return correct value
        Vx = Vx_k;
        Vy = Vy_k;

end
