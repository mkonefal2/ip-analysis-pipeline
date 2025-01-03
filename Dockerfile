FROM jenkins/jenkins:lts

USER root

# Instalacja Pythona i niezbędnych pakietów systemowych
RUN apt-get update && apt-get install -y python3 python3-pip python3-venv

# Tworzenie środowiska wirtualnego i instalacja pakietów
RUN python3 -m venv /opt/venv
ENV PATH="/opt/venv/bin:$PATH"

# Instalacja zależności w venv
RUN pip install --no-cache-dir duckdb geoip2 requests pandas

# Ustawienie katalogu roboczego
WORKDIR /var/jenkins_home

# Skopiowanie plików projektu
COPY . .

# Ustawienie Jenkins jako użytkownika domyślnego
USER jenkins
