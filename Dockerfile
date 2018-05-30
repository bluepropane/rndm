FROM python:3-onbuild
ENTRYPOINT ["/bin/bash", "-c"]
EXPOSE 8000
CMD [". /usr/src/app/start.sh"]