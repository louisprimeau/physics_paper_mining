import os, matplotlib
import numpy as np
import matplotlib.pyplot as plt

import layoutparser as lp
from PIL import Image
from pix2text import Pix2Text, merge_line_texts
from pdf2image import convert_from_path

from util import *

def analyze_pdf(path, layout_model, text_model,
                image_cleaning_pipeline=[], text_cleaning_pipeline=[]):

    page_images = [np.array(page_image) for page_image in convert_from_path(path, dpi=500)]

    output_text, output_images, figure_captions = [], [], []
    for i, page_image in enumerate(page_images[0:]):
        
        raw_layout = layout_model.detect(page_image)

        figure_layout = [block for block in raw_layout if block.type=='Figure']
        paragraph_layout = [block for block in raw_layout if block.type=='Text']

        paragraph_layout = reorganize_layout(paragraph_layout)
        caption_layout, paragraph_layout = associate_captions(paragraph_layout, figure_layout)

        figure_images = extract_image_from_image(figure_layout, page_image)

        page_text = extract_text_from_image(text_model,
                                            paragraph_layout,
                                            page_image,
                                            image_cleaning_pipeline,
                                            text_cleaning_pipeline)

        page_captions = extract_text_from_image(text_model,
                                                caption_layout,
                                                page_image,
                                                image_cleaning_pipeline,
                                                text_cleaning_pipeline)

        output_text += page_text
        output_images += figure_images
        figure_captions += page_captions

    return output_text, output_images, figure_captions
