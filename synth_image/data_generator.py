import os
import random as rnd

from PIL import Image, ImageFilter

from trdg import computer_text_generator, background_generator, distorsion_generator

BACKGROUND_WIDTH = 1024
BACKGROUND_HEIGHT = 800



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
        background_mask = Image.new(
            "RGB", (background_width, background_height), (0, 0, 0)
        )


    ##########################
        # Create picture of text #
        ##########################
        text_list = text.split("#_#")
        for text_index, text in enumerate(text_list):
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

            new_text_width, _ = resized_img.size

            background_img.paste(resized_img, (100, text_index * 50), resized_img)
            # background_mask.paste(resized_mask, (100, text_index * 50))


            ##################################
            # Apply gaussian blur #
            ##################################

            gaussian_filter = ImageFilter.GaussianBlur(
                radius=blur if not random_blur else rnd.randint(0, blur)
            )
            final_image = background_img.filter(gaussian_filter)
            # final_mask = background_mask.filter(gaussian_filter)



        #####################################
        # Generate name for resulting image #
        #####################################

        image_name = "{}.{}".format(str(index), extension)
        mask_name = "{}_mask.png".format(str(index))

        # Save the image
        final_image.convert("RGB").save(os.path.join(out_dir, image_name))
        # if output_mask == 1:
        #     final_mask.convert("RGB").save(os.path.join(out_dir, mask_name))

