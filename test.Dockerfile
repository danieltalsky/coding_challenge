FROM continuumio/miniconda:latest

WORKDIR /var

COPY environment.yml ./

RUN conda env create -f environment.yml

RUN echo "source activate user-profiles" &> ~/.bashrc
ENV PATH /opt/conda/envs/user-profiles/bin:$PATH

EXPOSE 5000

ENTRYPOINT ["python", "-m", "pytest"]