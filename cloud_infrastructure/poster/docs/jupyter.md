---
no_toc: True
slim: True
---
# Jupyter

The customization of Jupyter is not complicated however the explanation to the replacement of the [`login.py`](broken link) file is rather lengthy so please consult the accompanying proceedings paper.

To integrate Jupyter into this cloud architecture, the following steps are suggested

   * Replace the `login.py` file in the `site-packages` directory with the one provided [here](broken link)
   * Set the base_url variable appropriately
   * Validate the shared drive belongs to the current user (we used a read only `.id` file)
   * Generate a certificate (self-signed is adequate) so that Jupyter runs over HTTPS
   * Ensure health check is correctly configured (some Jupyter URL's generate a `302` code)

Return to [Authentication and Applications](integration.md)
