from setuptools import find_packages, setup
from glob import glob

package_name = 'turtle_exercise'

setup(
    name=package_name,
    version='0.0.0',
    packages=find_packages(exclude=['test']),
    data_files=[
        ('share/ament_index/resource_index/packages',
            ['resource/' + package_name]),
        ('share/' + package_name, ['package.xml']),
        ('share/' + package_name + '/launch', glob('launch/*.launch.py')),
    ],
    install_requires=['setuptools'],
    zip_safe=True,
    maintainer='y2x',
    maintainer_email='2839938306@qq.com',
    description='TODO: Package description',
    license='Apache-2.0',
    extras_require={
        'test': [
            'pytest',
        ],
    },
    entry_points={
        'console_scripts': [
            # "turtle_control = turtle_exercise.turtle_control:main"
            "turtle_spawn_service = turtle_exercise.turtle_spawn_service:main",
            "turtle_target_control = turtle_exercise.turtle_control_target:main"
        ],
    },
)
