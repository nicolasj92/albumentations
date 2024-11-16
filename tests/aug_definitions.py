import cv2
import numpy as np

import albumentations as A

AUGMENTATION_CLS_PARAMS = [
    [
        A.ImageCompression,
        {
            "quality_lower": 10,
            "quality_upper": 80,
            "compression_type": "webp",
        },
    ],
    [
        A.HueSaturationValue,
        {"hue_shift_limit": 70, "sat_shift_limit": 95, "val_shift_limit": 55},
    ],
    [A.RGBShift, {"r_shift_limit": 70, "g_shift_limit": 80, "b_shift_limit": 40}],
    [A.RandomBrightnessContrast, {"brightness_limit": 0.5, "contrast_limit": 0.8}],
    [A.Blur, {"blur_limit": 3}],
    [A.MotionBlur, {"blur_limit": 3}],
    [A.MedianBlur, {"blur_limit": 3}],
    [A.GaussianBlur, {"blur_limit": 3}],
    [A.GaussNoise, {"var_limit": (20, 90), "mean": 10, "per_channel": False}],
    [A.CLAHE, {"clip_limit": 2, "tile_grid_size": (12, 12)}],
    [A.RandomGamma, {"gamma_limit": (10, 90)}],
    [A.CoarseDropout, {"num_holes_range": (2, 5), "hole_height_range": (3, 4), "hole_width_range": (4, 6)}],
    [
        A.RandomSnow,
        {"snow_point_lower": 0.2, "snow_point_upper": 0.4, "brightness_coeff": 4},
    ],
    [
        A.RandomRain,
        {
            "slant_lower": -5,
            "slant_upper": 5,
            "drop_length": 15,
            "drop_width": 2,
            "drop_color": (100, 100, 100),
            "blur_value": 3,
            "brightness_coefficient": 0.5,
            "rain_type": "heavy",
        },
    ],
    [A.RandomFog, {"fog_coef_lower": 0.2, "fog_coef_upper": 0.8, "alpha_coef": 0.11}],
    [
        A.RandomSunFlare,
        {
            "flare_roi": (0.1, 0.1, 0.9, 0.6),
            "angle_range": (0.1, 0.95),
            "num_flare_circles_range": (7, 11),
            "src_radius": 300,
            "src_color": (200, 200, 200),
        },
    ],
    [
        A.RandomGravel,
        {
            "gravel_roi": (0.1, 0.4, 0.9, 0.9),
            "number_of_patches": 2,
        },
    ],
    [
        A.RandomShadow,
        {
            "shadow_roi": (0.1, 0.4, 0.9, 0.9),
            "num_shadows_limit": (2, 4),
            "shadow_dimension": 8,
        },
    ],
    [
        A.PadIfNeeded,
        {
            "min_height": 512,
            "min_width": 512,
            "border_mode": cv2.BORDER_CONSTANT,
            "value": (10, 10, 10),
        },
    ],
    [
        A.Rotate,
        {
            "limit": 120,
            "interpolation": cv2.INTER_CUBIC,
            "border_mode": cv2.BORDER_CONSTANT,
            "value": (10, 10, 10),
            "crop_border": False,
        },
    ],
    [
        A.SafeRotate,
        {
            "limit": 120,
            "interpolation": cv2.INTER_CUBIC,
            "border_mode": cv2.BORDER_CONSTANT,
            "value": (10, 10, 10),
        },
    ],
    [
        A.ShiftScaleRotate,
        {
            "shift_limit": (-0.2, 0.2),
            "scale_limit": (-0.2, 0.2),
            "rotate_limit": (-70, 70),
            "interpolation": cv2.INTER_CUBIC,
            "border_mode": cv2.BORDER_CONSTANT,
            "value": (10, 10, 10),
        },
    ],
    [
        A.ShiftScaleRotate,
        {
            "shift_limit_x": (-0.3, 0.3),
            "shift_limit_y": (-0.4, 0.4),
            "scale_limit": (-0.2, 0.2),
            "rotate_limit": (-70, 70),
            "interpolation": cv2.INTER_CUBIC,
            "border_mode": cv2.BORDER_CONSTANT,
            "value": (10, 10, 10),
        },
    ],
    [
        A.OpticalDistortion,
        {
            "distort_limit": 0.2,
            "shift_limit": 0.2,
            "interpolation": cv2.INTER_CUBIC,
            "border_mode": cv2.BORDER_CONSTANT,
            "value": (10, 10, 10),
        },
    ],
    [
        A.GridDistortion,
        {
            "num_steps": 10,
            "distort_limit": 0.5,
            "interpolation": cv2.INTER_CUBIC,
            "border_mode": cv2.BORDER_CONSTANT,
            "value": (10, 10, 10),
        },
    ],
    [
        A.ElasticTransform,
        {
            "alpha": 2,
            "sigma": 25,
            "interpolation": cv2.INTER_CUBIC,
            "border_mode": cv2.BORDER_CONSTANT,
            "value": (10, 10, 10),
        },
    ],
    [A.CenterCrop, {"height": 10, "width": 10}],
    [A.RandomCrop, {"height": 10, "width": 10}],
    [A.CropNonEmptyMaskIfExists, {"height": 10, "width": 10}],
    [A.RandomSizedCrop, {"min_max_height": (4, 8), "height": 10, "width": 10}],
    [A.Crop, {"x_max": 64, "y_max": 64}],
    [A.ToFloat, {"max_value": 16536}],
    [
        A.Normalize,
        {
            "mean": (0.385, 0.356, 0.306),
            "std": (0.129, 0.124, 0.125),
            "max_pixel_value": 100.0,
        },
    ],
    [A.RandomScale, {"scale_limit": 0.2, "interpolation": cv2.INTER_CUBIC}],
    [A.Resize, {"height": 64, "width": 64}],
    [A.SmallestMaxSize, {"max_size": 64, "interpolation": cv2.INTER_CUBIC}],
    [A.LongestMaxSize, {"max_size": 128, "interpolation": cv2.INTER_CUBIC}],
    [A.RandomGridShuffle, {"grid": (4, 4)}],
    [A.Solarize, {"threshold": 32}],
    [A.Posterize, {"num_bits": 1}],
    [A.Equalize, {"mode": "pil", "by_channels": False}],
    [
        A.MultiplicativeNoise,
        {"multiplier": (0.7, 2.3), "per_channel": True, "elementwise": True},
    ],
    [
        A.ColorJitter,
        {
            "brightness": [0.2, 0.3],
            "contrast": [0.7, 0.9],
            "saturation": [1.2, 1.7],
            "hue": [-0.2, 0.1],
        },
    ],
    [
        A.Perspective,
        {
            "scale": 0.5,
            "keep_size": False,
            "pad_mode": cv2.BORDER_REFLECT_101,
            "pad_val": 10,
            "mask_pad_val": 100,
            "fit_output": True,
            "interpolation": cv2.INTER_CUBIC,
        },
    ],
    [A.Sharpen, {"alpha": [0.2, 0.5], "lightness": [0.5, 1.0]}],
    [A.Emboss, {"alpha": [0.2, 0.5], "strength": [0.5, 1.0]}],
    [A.RandomToneCurve, {"scale": 0.2, "per_channel": False}],
    [A.RandomToneCurve, {"scale": 0.3, "per_channel": True}],
    [
        A.CropAndPad,
        {
            "px": 10,
            "keep_size": False,
            "sample_independently": False,
            "interpolation": cv2.INTER_CUBIC,
            "pad_cval_mask": [10, 20, 30],
            "pad_cval": [11, 12, 13],
            "pad_mode": cv2.BORDER_REFLECT101,
        },
    ],
    [
        A.Superpixels,
        {
            "p_replace": (0.5, 0.7),
            "n_segments": (20, 30),
            "max_size": 25,
            "interpolation": cv2.INTER_CUBIC,
        },
    ],
    [
        A.Affine,
        {
            "scale": 0.5,
            "translate_percent": 0.7,
            "translate_px": None,
            "rotate": 33,
            "shear": 21,
            "interpolation": cv2.INTER_CUBIC,
            "cval": 25,
            "cval_mask": 1,
            "mode": cv2.BORDER_CONSTANT,
            "fit_output": True,
        },
    ],
    [
        A.Affine,
        {
            "scale": {"x": [0.3, 0.5], "y": [0.1, 0.2]},
            "translate_percent": None,
            "translate_px": {"x": [10, 200], "y": [5, 101]},
            "rotate": [333, 360],
            "shear": {"x": [31, 38], "y": [41, 48]},
            "interpolation": 3,
            "cval": [10, 20, 30],
            "cval_mask": 1,
            "mode": cv2.BORDER_REFLECT,
            "fit_output": True,
        },
    ],
    [
        A.PiecewiseAffine,
        {
            "scale": 0.33,
            "nb_rows": (10, 20),
            "nb_cols": 33,
            "interpolation": 2,
            "mask_interpolation": 1,
            "cval": 10,
            "cval_mask": 20,
            "mode": "edge",
            "absolute_scale": True,
            "keypoints_threshold": 0.1,
        },
    ],
    [A.ChannelDropout, dict(channel_drop_range=(1, 2), fill_value=1)],
    [A.ChannelShuffle, {}],
    [A.Downscale, dict(scale_min=0.5, scale_max=0.75, interpolation=cv2.INTER_LINEAR)],
    [A.Flip, {}],
    [A.FromFloat, dict(dtype="uint8", max_value=1)],
    [A.HorizontalFlip, {}],
    [A.ISONoise, dict(color_shift=(0.2, 0.3), intensity=(0.7, 0.9))],
    [A.InvertImg, {}],
    [A.MaskDropout, dict(max_objects=2, image_fill_value=10, mask_fill_value=20)],
    [A.NoOp, {}],
    [
        A.RandomResizedCrop,
        dict(height=20, width=30, scale=(0.5, 0.6), ratio=(0.8, 0.9)),
    ],
    [A.FancyPCA, dict(alpha=0.3)],
    [A.RandomRotate90, {}],
    [A.ToGray, {}],
    [A.ToRGB, {}],
    [A.ToSepia, {}],
    [A.Transpose, {}],
    [A.VerticalFlip, {}],
    [A.RingingOvershoot, dict(blur_limit=(7, 15), cutoff=(np.pi / 5, np.pi / 2))],
    [
        A.UnsharpMask,
        {"blur_limit": 3, "sigma_limit": 0.5, "alpha": 0.2, "threshold": 15},
    ],
    [A.AdvancedBlur, dict(blur_limit=(3, 5), rotate_limit=(60, 90))],
    [A.PixelDropout, {"dropout_prob": 0.1, "per_channel": True, "drop_value": None}],
    [
        A.PixelDropout,
        {
            "dropout_prob": 0.1,
            "per_channel": False,
            "drop_value": None,
            "mask_drop_value": 15,
        },
    ],
    [
        A.RandomCropFromBorders,
        dict(crop_left=0.2, crop_right=0.3, crop_top=0.05, crop_bottom=0.5),
    ],
    [
        A.Spatter,
        dict(
            mean=0.2,
            std=0.1,
            gauss_sigma=3,
            cutout_threshold=0.4,
            intensity=0.7,
            mode="mud",
        ),
    ],
    [
        A.ChromaticAberration,
        dict(
            primary_distortion_limit=0.02,
            secondary_distortion_limit=0.05,
            mode="green_purple",
            interpolation=cv2.INTER_LINEAR,
        ),
    ],
    [A.Defocus, {"radius": (5, 7), "alias_blur": (0.2, 0.6)}],
    [A.ZoomBlur, {"max_factor": (1.56, 1.7), "step_factor": (0.02, 0.04)}],
    [
        A.XYMasking,
        {
            "num_masks_x": (1, 3),
            "num_masks_y": 3,
            "mask_x_length": (10, 20),
            "mask_y_length": 10,
            "mask_fill_value": 1,
            "fill_value": 0,
        },
    ],
    [
        A.PadIfNeeded,
        {
            "min_height": 512,
            "min_width": 512,
            "border_mode": 0,
            "value": [124, 116, 104],
            "position": "top_left",
        },
    ],
    [A.GlassBlur, dict(sigma=0.8, max_delta=5, iterations=3, mode="exact")],
    [
        A.GridDropout,
        dict(
            ratio=0.75,
            unit_size_range=(2, 10),
            shift_xy=(10, 20),
            random_offset=True,
            fill_value=10,
            mask_fill_value=20,
        ),
    ],
    [A.Morphological, {}],
    [A.D4, {}],
    [A.PlanckianJitter, {}],
    [A.OverlayElements, {}],
    [A.RandomCropNearBBox, {}],
    [
        A.TextImage,
        dict(
            font_path="./tests/filesLiberationSerif-Bold.ttf",
            font_size_range=(0.8, 0.9),
            color="red",
            stopwords=["a", "the", "is", "of", "it", "and", "to", "in", "on", "with", "for", "at", "by"],
        ),
    ],
    [A.GridElasticDeform, {"num_grid_xy": (10, 10), "magnitude": 10}],
    [A.ShotNoise, {"scale_range": (0.1, 0.3)}],
    [A.TimeReverse, {}],
    [A.TimeMasking, {"time_mask_param": 10}],
    [A.FrequencyMasking, {"freq_mask_param": 10}],
    [A.RandomJPEG, {"jpeg_quality": (50, 50)}],
    [A.RandomHorizontalFlip, {}],
    [A.RandomVerticalFlip, {}],
    [A.RandomGrayscale, {}],
    [A.RandomPerspective, {}],
    [A.RandomAffine, {}],
    [A.Pad, {"padding": 10}],
    [A.RandomRotation, {"degrees": 33}],
    [A.Erasing, {}],
    [A.RandomErasing, {}],
    [A.RandomInvert, {}],
    [A.RandomHue, {"hue": (-0.2, 0.2)}],
    [A.RandomClahe, {}],
    [A.RandomContrast, {"contrast": (0.8, 1.2)}],
    [A.RandomBrightness, {"brightness": (0.8, 1.2)}],
]
