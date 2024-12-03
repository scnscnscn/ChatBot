from setuptools import setup, find_packages
with open('README.md', encoding='utf-8') as f:
    long_description = f.read()
setup(
    name='Chatbot',
    version='0.1.0',
    author='Vincent Van',
    author_email='WLQVincent@outlook.com',
    description='Chatbot,weibo crawler,nlpmode training',
    long_description=open('README.md').read(),
    long_description_content_type='text/markdown',
    url='https://github.com/scnscnscn/ChatBot',
    packages=find_packages(),
    install_requires=[
        'openai',
        'python-docx',
        'transformers',
        'torch',
        'tensorflow',
        'opencv-python',
        'redis',
        'pandas',
        'matplotlib',
        'scikit-learn',
        'datasets'
    ],
    classifiers=[
        'Development Status :: 3 - Alpha',
        'Intended Audience :: Developers',
        'Topic :: Software Development :: Build Tools',
        'License :: OSI Approved :: MIT License',
    ],
    python_requires='>=3.8',
    keywords='Chatbot',
)
