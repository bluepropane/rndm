FROM python:3-onbuild
ENTRYPOINT ["/bin/bash", "-c"]
COPY start.sh /usr/src/app/start.sh
EXPOSE 8000
CMD [". /usr/src/app/start.sh"]