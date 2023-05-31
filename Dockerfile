FROM fluxrm/flux-sched:focal

# docker build -t flux_metrics_api .
# docker run -it -p 8443:8443 flux_metrics_api

LABEL maintainer="Vanessasaurus <@vsoch>"

USER root

# Assuming installing to /usr/local
ENV LD_LIBRARY_PATH=/usr/local/lib

WORKDIR /code
COPY . /code
RUN python3 -m pip install .
ENTRYPOINT ["flux", "start", "flux-metrics-api"]
CMD ["start"]
