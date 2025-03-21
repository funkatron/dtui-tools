# Draw Things JavaScript API Documentation

*Note: This documentation was machine-generated based on API analysis. Please verify functionality in your environment.*

## Table of Contents
- [Official Resources](#official-resources)
- [Community Resources](#community-resources)
- [Contributing](#contributing)
- [Quick Start Example](#quick-start-example)
- [Core Objects and Utilities](#core-objects-and-utilities)
  - [Console Functions](#console-functions)
  - [Device Information](#device-information)
  - [Random Number Generator](#random-number-generator)
  - [Geometric Classes](#geometric-classes)
    - [Point](#point)
    - [Size](#size)
    - [Rectangle](#rectangle)
  - [Image Metadata](#image-metadata)
- [Pipeline Control](#pipeline-control)
- [File System Access](#file-system-access)
- [Canvas Operations](#canvas-operations)
- [Mask Operations](#mask-operations)
- [UI Components](#ui-components)
- [Constants Usage](#constants-usage)
  - [Mask Value Types](#mask-value-types)
  - [Sampler Types](#sampler-types)
  - [Body Mask Types](#body-mask-types)

## Official Resources
- [Draw Things App](https://drawthings.ai)
- [Official Documentation](https://docs.drawthings.ai)
- [Community Scripts Repository](https://github.com/drawthingsai/community-scripts)
- [Community Documentation](https://github.com/drawthingsai/community-docs)

## Community Resources
- [Draw Things Discord](https://discord.gg/drawthings)
- [Community Scripts Examples](https://github.com/drawthingsai/community-scripts/tree/main/scripts)

## Contributing
To contribute to the Draw Things community:
1. Scripts: Submit PRs to [community-scripts](https://github.com/drawthingsai/community-scripts)
2. Documentation: Submit PRs to [community-docs](https://github.com/drawthingsai/community-docs)
3. Share your creations on Discord

## Quick Start Example
```javascript
// Simple image generation script with UI
const userInput = requestFromUser("My Generator", "", function() {
    return [
        this.section("Settings", "", [
            this.textField("a beautiful landscape", "Enter prompt", false, 60),
            this.slider(20, this.slider.fractional(0), 1, 50, "Steps"),
            this.switch(false, "Use random seed")
        ])
    ];
});

const prompt = userInput[0][0];
const steps = userInput[0][1];
const randomSeed = userInput[0][2];

const configuration = pipeline.configuration;
configuration.steps = steps;
if (randomSeed) configuration.seed = -1;

pipeline.run({
    configuration: configuration,
    prompt: prompt
});
```

## Core Objects and Utilities

### Console Functions
```javascript
// Log regular message
console.log("Generation started");

// Log object with formatting
console.log({
    prompt: "a cat",
    steps: 20,
    seed: 12345
});

// Log warning
console.warn("Model not found, using fallback");

// Log error
console.error("Generation failed");

// Open interactive REPL
console.repl();  // Useful for debugging
```

### Device Information
```javascript
// Get screen dimensions
const screen = device.screenSize;
console.log(`Screen size: ${screen.width}x${screen.height}`);

// Use for responsive UI calculations
const isLargeScreen = screen.width >= 1024;
```

### Random Number Generator
```javascript
// Create seeded RNG
const rng = new RNG(12345);

// Generate random numbers
const randomValue = rng.next();

// Use for consistent random selection
const options = ["cat", "dog", "bird"];
const randomChoice = options[rng.next() % options.length];
```

### Geometric Classes

#### Point
```javascript
// Create point
const center = new Point(100, 100);

// Use in canvas operations
canvas.moveCanvas(center.x, center.y);
```

#### Size
```javascript
// Create size
const imageSize = new Size(512, 512);

// Use for configuration
configuration.width = imageSize.width;
configuration.height = imageSize.height;
```

#### Rectangle
```javascript
// Create rectangle
const rect = new Rectangle(0, 0, 512, 512);

// Check intersection
const other = new Rectangle(100, 100, 200, 200);
const intersection = rect.intersect(other);
if (intersection) {
    console.log("Rectangles overlap");
}

// Scale rectangle
rect.scale(2.0);  // Double size

// Union of rectangles
const combined = Rectangle.union(rect, other);
```

### Image Metadata
```javascript
// Get image information
const metadata = new ImageMetadata(imageSrc);
console.log(`Image dimensions: ${metadata.width}x${metadata.height}`);

// Use for scaling calculations
const scaleFactor = 512 / metadata.width;
```

## Pipeline Control
```javascript
// Basic generation
pipeline.run({
    configuration: {
        width: 512,
        height: 512,
        steps: 20,
        seed: 12345,
        sampler: SamplerType.DPMPP_2M_KARRAS
    },
    prompt: "a beautiful sunset"
});

// Check and download models
const modelsNeeded = ["model1.safetensors", "model2.safetensors"];
if (!pipeline.areModelsDownloaded(modelsNeeded)) {
    pipeline.downloadBuiltins(modelsNeeded);
}

// Use LoRA
const lora = pipeline.findLoRAByName("style_lora");
if (lora) {
    configuration.loras = [lora];
}
```

## File System Access
```javascript
// List pictures
const pictures = filesystem.pictures.readEntries();
console.log("Available images:", pictures);

// Work with specific directory
const outputs = filesystem.pictures.readEntries("outputs");
for (const file of outputs) {
    console.log(`Found file: ${file}`);
}

// Get pictures directory path
const savePath = `${filesystem.pictures.path}/my_generation`;
```

## Canvas Operations
```javascript
// Basic canvas manipulation
canvas.clear();
canvas.canvasZoom = 1.5;
canvas.moveCanvas(0, 0);

// Load and save images
canvas.loadImage("input.png");
canvas.saveImage("output.png", false);

// Work with masks
const mask = canvas.createMask(512, 512, MaskValueType.PURE_NOISE);
mask.fillRectangle(0, 0, 256, 256, MaskValueType.MASK);

// Use AI features
const faces = canvas.detectFaces();
console.log(`Detected ${faces.length} faces`);

// Work with moodboard
canvas.addToMoodboardFromPhotos();
canvas.setMoodboardImageWeight(0.8, 0);
```

## Mask Operations
```javascript
// Create and modify mask
const mask = canvas.createMask(512, 512, MaskValueType.PURE_NOISE);
mask.fillRectangle(100, 100, 300, 300, MaskValueType.MASK);

// Use body mask
const bodyMask = canvas.bodyMask([BodyMaskType.UPPER_BODY], 10);
if (bodyMask) {
    console.log("Body detected and masked");
}
```

## UI Components
```javascript
// Basic dialog
const result = requestFromUser("Settings", "OK", function() {
    return [
        this.section("Basic", "", [
            this.textField("", "Enter text", false, 60),
            this.slider(20, this.slider.fractional(0), 1, 50, "Value")
        ])
    ];
});

// Complex UI with multiple components
const advanced = requestFromUser("Advanced Settings", "Generate", function() {
    return [
        this.section("Image", "", [
            this.size(512, 512, 64, 2048),
            this.imageField("Reference", false)
        ]),
        this.section("Parameters", "", [
            this.comboBox("DPMPP_2M_KARRAS", Object.keys(SamplerType)),
            this.doubleSlider([0.3, 0.7], this.slider.fractional(0), 0, 1, "Range"),
            this.switch(true, "Enable feature")
        ]),
        this.section("Help", "", [
            this.markdown("**Bold** and *italic* text"),
            this.image("help.png", 200, false)
        ])
    ];
});
```

## Constants Usage

### Mask Value Types
```javascript
// Create mask with different values
const noiseMask = canvas.createMask(512, 512, MaskValueType.PURE_NOISE);
const retainMask = canvas.createMask(512, 512, MaskValueType.RETAIN_OR_MASK);
```

### Sampler Types
```javascript
// Configure different samplers
configuration.sampler = SamplerType.DPMPP_2M_KARRAS;
configuration.sampler = SamplerType.EULER_A;

// List available samplers
const samplerNames = Object.keys(SamplerType);
```

### Body Mask Types
```javascript
// Create specific body masks
const clothingMask = canvas.bodyMask([BodyMaskType.CLOTHING], 5);
const upperBodyMask = canvas.bodyMask([BodyMaskType.UPPER_BODY], 10);
const fullBodyMask = canvas.bodyMask([
    BodyMaskType.UPPER_BODY,
    BodyMaskType.LOWER_BODY,
    BodyMaskType.NECK
], 5);
```
