## Usage

```
make init
pytest -s test_orthanc_rest_api.py --url <url> --port <port> --user <user> --password <password>
```

## Description

Performs testing of the 3 interfaces of an Orthanc installation:
* DICOM DIMSE
* DICOMWeb
* Orthanc REST API

## Data

Sample DICOM series are downloaded from the Cancer Imaging Archive (TCIA).  Each series is stored in a subdirectory of the `data/` directory, and cached in a subdirectory named for the SeriesInstaceUID of the series.  At each invocation, the TCIA is queried for the size and count of the series to be used, and this is compared against the cached files.  If there is an exact match, the series is not re-downloaded from TCIA.

## Citations

This software uses the 'Lung Phantom', 'PDMR-292921-168-R', and 'RIDER Phantom MRI' collections from the Cancer Imaging Archive (TCIA) public datasets
https://wiki.cancerimagingarchive.net/display/Public/Lung+Phantom#19038256ab660407d4df4523bcaf4a8cd0a7c816

### Data Citations

* Zhao, Binsheng. (2015). Data From Lung_Phantom. The Cancer Imaging Archive. https://doi.org/10.7937/K9/TCIA.2015.08A1IXOO
* Tatum, J., Kalen, J., Ileva, lilia, L, R., S, K., N, P., Jacobs, P., Sanders, C., A, J., Difilippantonio, S., L, T., hollingshead, melinda, J, P., Y, E., Clunie, D., Y, L., Suloway, C., Smith, K., U, W., … Doroshow, J. (n.d.). Imaging characterization of a metastatic patient derived model of adenocarcinoma pancreas: PDMR-292921-168-R. The Cancer Imaging Archive. https://doi.org/10.7937/TCIA.2020.PCAK-8Z10
* Jackson, Edward F. (2015). Data From RIDER_PHANTOM_MRI. The Cancer Imaging Archive. https://doi.org/10.7937/K9/TCIA.2015.MI4QDDHU

### TCIA Citation

Clark K, Vendt B, Smith K, Freymann J, Kirby J, Koppel P, Moore S, Phillips S, Maffitt D, Pringle M, Tarbox L, Prior F. 
The Cancer Imaging Archive (TCIA): Maintaining and Operating a Public Information Repository
Journal of Digital Imaging, Volume 26, Number 6, December, 2013, pp 1045-1057. https://doi.org/10.1007/s10278-013-9622-7