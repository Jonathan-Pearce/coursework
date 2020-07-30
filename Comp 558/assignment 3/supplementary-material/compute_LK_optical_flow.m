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

switch type_LK

    case "LK_naive"
        % YOUR IMPLEMENTATION GOES HERE

    case "LK_iterative"
        % YOUR IMPLEMENTATION GOES HERE

    case "LK_pyramid"
        % YOUR IMPLEMENTATION GOES HERE

end
