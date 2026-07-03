import torch
from transformers import CLIPProcessor, CLIPModel


class ClipModel:

    def __init__(self):
        self.device = "cuda" if torch.cuda.is_available() else "cpu"

        print(f"Using device: {self.device}")

        self.model = CLIPModel.from_pretrained(
            "openai/clip-vit-base-patch32"
        ).to(self.device)

        self.processor = CLIPProcessor.from_pretrained(
            "openai/clip-vit-base-patch32"
        )

    def encode_image(self, image):
        inputs = self.processor(
            images=image,
            return_tensors="pt"
        )

        pixel_values = inputs["pixel_values"].to(self.device)

        with torch.no_grad():
            output = self.model.get_image_features(
                pixel_values=pixel_values
            )

        if hasattr(output, "pooler_output"):
            features = output.pooler_output
        elif hasattr(output, "last_hidden_state"):
            features = output.last_hidden_state.mean(dim=1)
        else:
            features = output

        features = features / torch.norm(
            features,
            dim=-1,
            keepdim=True
        )

        return features.cpu().numpy().flatten()