---
no_toc: True
slim: True
---
# Jupyter

The customization of Jupyter is not complicated however the explanation to the replacement of the [`login.py`](https://github.com/WestHealth/scipy2020/tree/master/cloud_infrastructure/supplemental_code/jupyter/login.py) file is rather lengthy so please consult the accompanying proceedings paper.

To integrate Jupyter into this cloud architecture, the following steps are suggested

   * Replace the `login.py` file in the `site-packages` directory with the one provided [here](https://github.com/WestHealth/scipy2020/tree/master/cloud_infrastructure/supplemental_code/jupyter/login.py)
   * Set the base_url variable appropriately
   * Validate the shared drive belongs to the current user (we used a read only `.id` file)
   * Generate a certificate (self-signed is adequate) so that Jupyter runs over HTTPS
   * Ensure health check is correctly configured (some Jupyter URL's generate a `302` code)

Return to [Authentication and Applications](integration.md)
