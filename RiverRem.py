import streamlit as st
import os
from osgeo import gdal
from riverrem.REMMaker import REMMaker
import tempfile
from tempfile import NamedTemporaryFile


st.set_page_config(layout="wide")


st.set_option('deprecation.showPyplotGlobalUse', False)

def main():
        """River Rem App with Streamlit """

        url = "https://github.com/klarrieu/RiverREM"

        st.title("Relative Elevation Model Creator using RiverRem")
        st.write("Streamlit app using the River REM Python package by Kenneth Larrieu and Open Topography: [Link to GitHub Page](%s)" % url)
        activities = ["River REM", "About"]
        choice = st.sidebar.selectbox("Select Activities", activities)


        if choice == 'River REM':
            st.subheader("River REM")

            st.write("RiverREM is a Python package created by Kenneth Larrieu to automatically create river relative elevation model (REM) visualisations "
                     "with just a input digital elevation model (DEM). For this page, only use onshore DEMs as the package uses the OpenStreetMap API to retrieve"
                     " river centerline geometries over the DEM extent. "
                     "The package will interpolate river elevations automatically by using a sampling scheme based on raster resolution and river sinuosity to create high-resolution visualizations "
                     "without interpolation artefacts straight out of the box and without additional manual steps.")
            st.write("See the 'About' section using the drop down list to the left for more information on the package and where to find DEMs to try this tool out")
            st.write(
                "The GeoTiff size is limited to 200MB and requires geolocation coordinates, if the REM process is taking longer than expected please use the 'STOP' button on the left when it appears or refresh the page.")

            # If CSV is not uploaded and checkbox is filled, use values from the example file
            # and pass them down to the next if block
            use_example_filea = st.checkbox(
                "Use example digital elevation .tif file", True, help="Use in-built example file to demo the app")

            if use_example_filea:
                SRTM = "EXAMPLE_DEM.tif"

            uploadeda = st.file_uploader("Choose a tif file", type=["tif"])
            if uploadeda is not None:
                with NamedTemporaryFile("wb", suffix=".tif", delete=False) as f:
                    f.write(uploadeda.getvalue())
                    SRTM = f.name
                    # f.name is the path of the temporary file

            colour_ramp1 = st.text_input('Choose colour-ramp (default is mako_r, see link for more styles such as magma_r, crest_r: https://seaborn.pydata.org/tutorial/color_palettes.html', 'mako_r')

            if st.button("Create REM, this may take a few minutes"):
                stop = st.sidebar.button("Stop")
                if stop:
                    st.stop()
                with st.spinner('Wait for it...'):

                    temp_dir = tempfile.TemporaryDirectory()
                    temp_dir_path = temp_dir.name
                # provide the DEM file path and desired output directory
                    rem_maker = REMMaker(dem=SRTM, out_dir=temp_dir_path, workers=-1)
                # create an REM
                    rem_maker.make_rem()
                # create an REM visualization with the given colormap
                    rem_maker.make_rem_viz(cmap=colour_ramp1)
                    for filename in os.listdir(temp_dir_path):
                        if filename.endswith('.png'):
                            image_path = os.path.join(temp_dir_path, filename)
                    from PIL import Image

                    image = Image.open(image_path)
                    st.image(image)

                    st.download_button(label='Download Image as PNG',
                                       data=open(image_path, 'rb').read(),
                                       file_name='imagename.png',
                                       mime='image/png')
                    st.download_button(label='Download Image as TIF',
                                       data=open(image_path, 'rb').read(),
                                       file_name='imagename.tif',
                                       mime='image/png')
                    st.button(label='Clear Cache')
                    temp_dir.cleanup()

        elif choice == 'About':
            from PIL import Image
            imageREM = Image.open('yukon_crop.png')
            st.image(imageREM, caption="REM of the Yukon River, North America by the Kenneth Larrieu [Link to GitHub Page](%s)" % url)

            st.subheader("About")
            url2 = "https://github.com/DahnJ/REM-xarray"
            url3 = "https://github.com/DahnJ/Awesome-DEM"
            url4 = "https://opentopography.org/"
            url5 = "https://apps.nationalmap.gov/downloader/"
            url6 = "https://emodnet.ec.europa.eu/geoviewer/"
            st.write("This app was made to help provide greater access to the RiverRem package for non-python users.")
            st.write("RiverREM is a Python package created by Kenneth Larrieu to automatically create river relative elevation model (REM) visualisations "
                     "with just a input digital elevation model (DEM). The idea is to allow users to quickly use and try the package out without any coding experience. "
                     "The package uses the OpenStreetMap API to retrieve river centerline geometries over the DEM extent. "
                     "More functionality is offered by the package not shown here and can be found in the documentation in package's GitHub page")

            st.write("To find a DEM for your area of interest the following links may be of interest for free topography and bathymetric data:")
            st.write("[Link of DEM websites](%s)" % url3)
            st.write("[Link to OpenTopography](%s)" % url4)
            st.write("[Link to USGS](%s)" % url5)
            st.write("[Link to EMODnet](%s)" % url6)

            st.subheader("References")
            st.write("Credit and references goes to Kenneth Larrieu and Open Topography for creating the RiverREM package and Streamlit for making this app a possibility [Link to GitHub Page](%s)" % url)
            st.write("Image from REM-xarray github page by Daniel Jahn [Link to GitHub Page](%s)" % url2)



if __name__ == '__main__':
    main()
