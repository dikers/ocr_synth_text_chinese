import os
import random as rnd
import random

from PIL import Image, ImageFilter

from trdg import computer_text_generator, background_generator, distorsion_generator

BACKGROUND_WIDTH = 1280
BACKGROUND_HEIGHT = 720



class FakeTextDataGenerator(object):
    @classmethod
    def generate_from_tuple(cls, t):
        """
            Same as generate, but takes all parameters as one tuple
        """
        cls.generate(*t)


    @classmethod
    def generate(
        cls,
        index,
        text,
        font,
        out_dir,
        size,

        extension,
        skewing_angle,
        random_skew,
        blur,
        random_blur,

        background_type,
        distorsion_type,
        distorsion_orientation,
        name_format,

        width,
        alignment,
        text_color,
        orientation,
        space_width,

        character_spacing,
        margins,
        fit,
        output_mask,
        word_split,

        image_dir,
    ):
        margin_top, margin_left, margin_bottom, margin_right = margins
        horizontal_margin = margin_left + margin_right

        background_width = BACKGROUND_WIDTH
        background_height = BACKGROUND_HEIGHT

        #############################
        # Generate background image #
        #############################

        background_type = random.randint(0, 1)
        if background_type == 0:
            background_img = background_generator.gaussian_noise(
                background_height, background_width
            )
        elif background_type == 1:
            background_img = background_generator.plain_white(
                background_height, background_width
            )
        elif background_type == 2:
            background_img = background_generator.quasicrystal(
                background_height, background_width
            )
        else:
            background_img = background_generator.image(
                background_height, background_width, image_dir
            )
        # background_mask = Image.new(
        #     "RGB", (background_width, background_height), (0, 0, 0)
        # )


        ##########################
        # Create picture of text #
        ##########################
        text_list = text.split("#_#")
        last_text_right = 10
        last_text_top = 10
        label_lines = ''
        for text_index, text in enumerate(text_list):
            text.replace(',', '，')
            image, mask = computer_text_generator.generate(
                text,
                font,
                text_color,
                size,
                orientation,
                space_width,
                character_spacing,
                fit,
                word_split,
            )
            random_angle = rnd.randint(0 - skewing_angle, skewing_angle)
            rotated_img = image.rotate(skewing_angle if not random_skew else random_angle, expand=1)
            rotated_mask = mask.rotate(skewing_angle if not random_skew else random_angle, expand=1)


            #############################
            # Apply distorsion to image #
            #############################
            distorsion_type = random.randint(0, 2)

            if distorsion_type == 0:
                distorted_img = rotated_img  # Mind = blown
                distorted_mask = rotated_mask
            elif distorsion_type == 1:
                distorted_img, distorted_mask = distorsion_generator.sin(
                    rotated_img,
                    rotated_mask,
                    vertical=(distorsion_orientation == 0 or distorsion_orientation == 2),
                    horizontal=(distorsion_orientation == 1 or distorsion_orientation == 2),
                )
            elif distorsion_type == 2:
                distorted_img, distorted_mask = distorsion_generator.cos(
                    rotated_img,
                    rotated_mask,
                    vertical=(distorsion_orientation == 0 or distorsion_orientation == 2),
                    horizontal=(distorsion_orientation == 1 or distorsion_orientation == 2),
                )
            else:
                distorted_img, distorted_mask = distorsion_generator.random(
                    rotated_img,
                    rotated_mask,
                    vertical=(distorsion_orientation == 0 or distorsion_orientation == 2),
                    horizontal=(distorsion_orientation == 1 or distorsion_orientation == 2),
                )

            ##################################
            # Resize image to desired format #
            ##################################

            # Horizontal text
            new_width = int(
                distorted_img.size[0]
                * (float(size) / float(distorted_img.size[1]))
            )
            resized_img = distorted_img.resize(
                (new_width, size), Image.ANTIALIAS
            )

            #############################
            # Place text with alignment #
            #############################

            gaussian_filter = ImageFilter.GaussianBlur(
                radius=blur if not random_blur else rnd.randint(0, blur)
            )
            resized_img = resized_img.filter(gaussian_filter)



            text_width, text_height = resized_img.size

            text_left, text_top = cls.generate_position(last_text_right, last_text_top,
                                                        text_width, text_height)

            label_lines += cls.generate_label(text_left, text_top, text_width, text_height, text)+'\n'

            if text_left <= 0:
                # print("[warning]  text too large ")
                break

            background_img.paste(resized_img, (text_left, text_top), resized_img)
            last_text_right = text_left + text_width
            last_text_top = text_top


        #####################################
        # Generate name for resulting image #
        #####################################
        image_name = "{}.{}".format(str(index), extension)
        label_name = "{}.{}".format(str(index), 'txt')
        # Save the image

        images_dir = os.path.join(out_dir, 'images')
        labels_dir = os.path.join(out_dir, 'labels')

        with open(os.path.join(labels_dir, label_name), "w", encoding='utf-8') as f:
            f.write(label_lines)

        background_img.convert("RGB").save(os.path.join(images_dir, image_name))



    @classmethod
    def generate_position(cls, last_text_right, last_text_top,
                          text_width, text_height):
        left = last_text_right + random.randint(50, 100)

        if left + text_width > BACKGROUND_WIDTH:
            left = 10 + random.randint(5, 20)
            top = last_text_top + text_height + random.randint(10, 30)
        else:
            top = last_text_top

        if top + text_height > BACKGROUND_HEIGHT:
            return -1, -1

        return left, top

    @classmethod
    def generate_label(cls, left, top, text_width, text_height, text):
        # 顺时针 从left_top 开始
        x_1 = left
        y_1 = top

        x_2 = left + text_width
        y_2 = top

        x_3 = left + text_width
        y_3 = top + text_height

        x_4 = left
        y_4 = top + text_height
        line = '{},{},{},{},{},{},{},{},{}'.format(x_1, y_1,
                                                   x_2, y_2,
                                                   x_3, y_3,
                                                   x_4, y_4,
                                                   text)
        return line