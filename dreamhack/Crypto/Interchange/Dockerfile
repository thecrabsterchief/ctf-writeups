FROM ubuntu:20.04

# Setup environ
ENV user interchange
ENV prob_port 13111

# Install packages
RUN apt-get update
RUN apt-get install -y socat python3 pip
RUN pip install pycrypto

# Change permission
RUN chmod 1733 /tmp /var/tmp /dev/shm

# Additional configuration
RUN adduser $user
ADD ./chal.py /home/$user/chal.py
ADD ./cipher.py /home/$user/cipher.py
ADD ./flag /home/$user/flag

RUN chown -R root:root /home/$user/
RUN chown root:$user /home/$user/chal.py
RUN chown root:$user /home/$user/cipher.py
RUN chown root:$user /home/$user/flag

RUN chmod 2755 /home/$user/chal.py
RUN chmod 2755 /home/$user/cipher.py
RUN chmod 440 /home/$user/flag

# final
WORKDIR /home/$user
CMD socat -T 60 TCP-LISTEN:$prob_port,reuseaddr,fork EXEC:/home/$user/chal.py
USER $user
EXPOSE $prob_port
