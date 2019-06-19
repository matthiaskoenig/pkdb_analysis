from setuptools import setup, find_packages

setup(name='pkdb_analysis',
      version='1.0',
      packages=find_packages(),
      package_data={
            '': ['requirements.txt'],
          },
      include_package_data=True,
      zip_safe=False,
      entry_points={'console_scripts': ['watch_study = data_management.watch_study:main'], },
      )