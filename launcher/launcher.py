import client.coap_obs_get_client
import client.coap_post_client
import robot_cleaner_coap_process

if __name__ == "__main__":
    robot_cleaner_coap_process.run()  # start server
    client.coap_obs_get_client.run()  # get observation
    client.coap_post_client.run()   #   post client [error]