#include <iostream>
#include <opencv2/opencv.hpp>

using namespace std;
using namespace cv;

extern "C" {

// Simple math function
int add(int a, int b) {
    return a + b;
}

// Simple print function
void say_hello() {
    std::cout << "Hello from C++!" << std::endl;
}

// Helper function: Write frames between specific start and end frame
void writeFrames(VideoCapture &cap, VideoWriter &writer, int startFrame, int endFrame) {
    cap.set(CAP_PROP_POS_FRAMES, startFrame);
    int currentFrame = startFrame;
    Mat frame;
    while (cap.read(frame)) {
        if (endFrame != -1 && currentFrame > endFrame) break;
        writer.write(frame);
        currentFrame++;
    }
}

// Main video editing function
int edit_video(const char* mainVideoPath, const char* sponsorVideoPath, const char* outputPath, double cutTimeSeconds) {
    // Open main video
    VideoCapture mainCap(mainVideoPath);
    if (!mainCap.isOpened()) {
        cerr << "Error: Cannot open main video file: " << mainVideoPath << endl;
        return -1;
    }

    // Open sponsor video
    VideoCapture sponsorCap(sponsorVideoPath);
    if (!sponsorCap.isOpened()) {
        cerr << "Error: Cannot open sponsor video file: " << sponsorVideoPath << endl;
        return -1;
    }

    // Get main video properties
    int width = (int)mainCap.get(CAP_PROP_FRAME_WIDTH);
    int height = (int)mainCap.get(CAP_PROP_FRAME_HEIGHT);
    double fps = mainCap.get(CAP_PROP_FPS);
    int fourcc = VideoWriter::fourcc('m','p','4','v');
    int totalFrames = (int)mainCap.get(CAP_PROP_FRAME_COUNT);

    // Calculate frame number where cut happens
    int cutFrame = (int)(cutTimeSeconds * fps);
    if (cutFrame >= totalFrames) {
        cerr << "Error: Cut time is beyond the video length." << endl;
        return -1;
    }

    // Prepare writer
    VideoWriter writer(outputPath, fourcc, fps, Size(width, height));
    if (!writer.isOpened()) {
        cerr << "Error: Cannot create output video file: " << outputPath << endl;
        return -1;
    }

    cout << "Editing video..." << endl;
    cout << "Main video cut at frame: " << cutFrame << " (time: " << cutTimeSeconds << "s)" << endl;

    // 1. Write first part of main video
    writeFrames(mainCap, writer, 0, cutFrame);

    // 2. Write sponsor video completely
    sponsorCap.set(CAP_PROP_POS_FRAMES, 0);
    Mat frame;
    while (sponsorCap.read(frame)) {
        // Resize sponsor to match main video size if different
        if (frame.size() != Size(width, height)) {
            resize(frame, frame, Size(width, height));
        }
        writer.write(frame);
    }

    // 3. Write remaining part of main video
    writeFrames(mainCap, writer, cutFrame + 1, -1);

    cout << "Video editing complete! Saved to: " << outputPath << endl;
    return 0;
}

} // extern "C"
