FROM gdoteof/ghc:7.8.3

RUN apt-get update && apt-get install -y \
	xvfb \
	libgtk2.0 \
	x11vnc \
	ratpoison

ADD http://c758482.r82.cf2.rackcdn.com/sublime-text_build-3065_amd64.deb sublime-text.deb
RUN dpkg -i sublime-text.deb

ADD startXvfb.sh startXvfb.sh
RUN chmod +x startXvfb.sh

# Expose vnc port
EXPOSE 5900

ENV SUBLIME_PATH=subl
ENV DISPLAY :0