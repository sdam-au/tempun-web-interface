# Web interface for Monte Carlo modelling of historical datasets with a high level of temporal uncertainty
[![DOI](https://zenodo.org/badge/DOI/10.5281/zenodo.XXXXXX.svg)](https://doi.org/10.5281/zenodo.XXXXXX)
[![Hugging Face Spaces](https://img.shields.io/badge/%F0%9F%A4%97%20Hugging%20Face-Spaces-blue)](https://huggingface.co/spaces/petrifiedvoices/tempun)

## Description

This tool provides an accessible web interface for running Monte Carlo simulations on historical datasets with temporal uncertainty using the [tempun](https://pypi.org/project/tempun/) Python package. Users can upload their own datasets, configure simulation parameters, customise visualisations, and download results, including processed data and reproducible Python scripts.

## Features

- Upload CSV or Excel files with temporal data
- Configure simulation parameters (temporal range, bin size, number of iterations)
- Customisable visualisation labels
- Download visualisations (PNG format)
- Download processed data with random dates (CSV format)
- Download reproducible Python script with complete metadata and provenance information
- No installation required - runs entirely in the browser

## Live Demo

Access the tool at: https://huggingface.co/spaces/petrifiedvoices/tempun

## Data Requirements

Your input file must contain:
- At least two columns with temporal information (start and end dates)
- Dates formatted as years (YYYY format)
- Years BCE as negative values, CE as positive values
- Column names can be specified in the interface (default: `not_before` and `not_after`)

## Usage

1. Upload a CSV or Excel file containing temporal data
2. Select columns containing start dates (not_before) and end dates (not_after)
3. Set temporal parameters (start year, end year, bin size)
4. Set simulation size (number of random dates per record)
5. Customise visualisation labels (optional)
6. Click "Run Simulation"
7. Download visualisation, processed data, and Python script

## Limitations

This web interface is designed for datasets with up to 5,000 records. For larger datasets, please use the [tempun package](https://github.com/sdam-au/tempun_demo) locally.

## Technical Details

- **Built with**: [Gradio](https://gradio.app/) 
- **Core package**: [tempun](https://pypi.org/project/tempun/) by Vojtěch Kaše
- **Visualisation**: Matplotlib with Calibri font
- **Programming language**: Python

## Authors

**Petra Heřmánková** (Web Interface Developer)
- ORCID: [0000-0002-6349-0540](https://orcid.org/0000-0002-6349-0540)
- Affiliation: Assistant Professor, Aarhus University, Department of History and Classical Studies
- GitHub: [@petrifiedvoices](https://github.com/petrifiedvoices)

**Vojtěch Kaše** (tempun Package Author)
- ORCID: [0000-0002-6601-1605](https://orcid.org/0000-0002-6601-1605)
- Affiliation: Aarhus University / University of West Bohemia
- tempun package: https://pypi.org/project/tempun/

**Adéla Sobotkova** (Contributor)
- ORCID: [0000-0002-4541-3963](https://orcid.org/0000-0002-4541-3963)
- Affiliation: Aarhus University

## Cite Us

If you use this tool in your research, please cite both the web interface and the underlying tempun package:

### BibTeX

```bibtex
@software{hermankova2025tempun,
  author       = {Heřmánková, Petra},
  title        = {Tempun Web Interface},
  year         = 2025,
  publisher    = {Zenodo},
  doi          = {10.5281/zenodo.XXXXXX},
  url          = {https://doi.org/10.5281/zenodo.XXXXXX}
}

@software{kase2022tempun,
  author       = {Kaše, Vojtěch},
  title        = {tempun},
  year         = 2022,
  publisher    = {Zenodo},
  version      = {v0.2.2},
  doi          = {10.5281/zenodo.8179346},
  url          = {https://doi.org/10.5281/zenodo.8179346}
}
```

### Text Citations

- Heřmánková, P. (2025). *Tempun Web Interface* [Software]. Zenodo. https://doi.org/10.5281/zenodo.XXXXXX
- Kaše, V. (2022). *tempun* (Version v0.2.2) [Software]. Zenodo. https://zenodo.org/records/8179346

## Licence

This work is licensed under a [Creative Commons Attribution-ShareAlike 4.0 International License](https://creativecommons.org/licenses/by-sa/4.0/).

[![CC BY-SA 4.0](https://licensebuttons.net/l/by-sa/4.0/88x31.png)](https://creativecommons.org/licenses/by-sa/4.0/)

## Related Publications

Kaše, Vojtěch, Adéla Sobotkova, and Petra Heřmánková. 2023. 'Modeling Temporal Uncertainty in Historical Datasets'. *Proceedings of the Computational Humanities Research Conference 2023*, 413–25. https://ceur-ws.org/Vol-3558/paper5123.pdf

## Acknowledgements

This tool builds upon the [tempun package](https://pypi.org/project/tempun/) developed by Vojtěch Kaše. 

## Links

- Live tool: https://huggingface.co/spaces/petrifiedvoices/tempun
- tempun package: https://pypi.org/project/tempun/
- tempun demo: https://github.com/sdam-au/tempun_demo
- Documentation: https://ceur-ws.org/Vol-3558/paper5123.pdf 

## Contributing

Contributions, issues, and feature requests are welcome! Feel free to check the [issues page](https://github.com/yourusername/tempun-web-interface/issues).

## Support

If you encounter any issues or have questions:
- Open an issue on [GitHub](https://github.com/yourusername/tempun-web-interface/issues)
