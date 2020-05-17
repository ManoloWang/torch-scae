import unittest

import torch

from torch_scae.configs import mnist_config
from torch_scae.part_encoder import CNNEncoder, CapsuleImageEncoder


class CapsuleImageEncoderTestCase(unittest.TestCase):
    def test_cnn_encoder(self):
        config = mnist_config
        cnn_encoder = CNNEncoder(
            **config.pcae_cnn_encoder
        )

        with torch.no_grad():
            batch_size = 4
            image = torch.rand(batch_size, *config.image_shape)
            out = cnn_encoder(image)
            self.assertTrue(
                list(out.shape) == [batch_size] + list(cnn_encoder.output_shape)
            )

    def test_pcae_primary_capsule(self):
        config = mnist_config
        cnn_encoder = CNNEncoder(
            **config.pcae_cnn_encoder
        )
        capsule_image_encoder = CapsuleImageEncoder(
            encoder=cnn_encoder,
            **config.pcae_primary_capsule
        )

        n_caps = config.pcae_primary_capsule.n_caps
        n_poses = config.pcae_primary_capsule.n_poses
        n_special_features = config.pcae_primary_capsule.n_special_features
        with torch.no_grad():
            batch_size = 4
            image = torch.rand(batch_size, *config.image_shape)
            result = capsule_image_encoder(image)

            self.assertTrue(
                tuple(result.pose.shape) == (batch_size, n_caps, n_poses)
            )
            self.assertTrue(
                tuple(result.feature.shape) == (batch_size, n_caps, n_special_features)
            )
            self.assertTrue(
                tuple(result.presence.shape) == (batch_size, n_caps)
            )
            self.assertTrue(
                tuple(result.presence_logit.shape) == (batch_size, n_caps)
            )
            self.assertTrue(
                list(result.img_embedding.shape) == [batch_size] + list(cnn_encoder.output_shape)
            )


if __name__ == '__main__':
    unittest.main()