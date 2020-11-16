
/*
 * ALL FROM
 * https://blog.mbedded.ninja/programming/operating-systems/linux/linux-serial-ports-using-c-cpp/#basic-setup-in-c
 *
 */

// C library headers
#include <stdio.h>
#include <string.h>
#include <stdint.h>
#include <unistd.h>

// Linux headers
#include <fcntl.h> // Contains file controls like O_RDWR
#include <errno.h> // Error integer and strerror() function
#include <termios.h> // Contains POSIX terminal control definitions
#include <unistd.h> // write(), read(), close()

// my headers
#include "mySerial_ROS.h"

char rx_buf[4]; // buffer per la ricezione seriale


int main(int argc, char **argv)
{
	ros::init(argc, argv, "Serial_Manager");
  	ros::NodeHandle n;
  


	//ros::Subscriber forward_mean0 = n.subscribe<geometry_msgs::Point>("/tag0_mean", 1, &Mean_forward);
	//ros::Subscriber backward_mean1 = n.subscribe<geometry_msgs::Point>("/tag1_mean", 1, &Mean_back);
	ros::Subscriber robot_pose = n.subscribe<geometry_msgs::Point>("/robot_pose", 1, &robot_pose_cb);
	ros::Subscriber forward_pose_topic = n.subscribe<geometry_msgs::PoseStamped>("/tag0_pose_f", 1, &Pose_cb_forward);
	ros::Subscriber backward_pose_topic = n.subscribe<geometry_msgs::PoseStamped>("/tag1_pose_f", 1, &Pose_cb_back);
	ros::Subscriber waypoint = n.subscribe<geometry_msgs::Point>("/waypoint_publisher", 1, &waypoint_cb);
	ros::Subscriber start_and_stop = n.subscribe<std_msgs::Float64>("/start_and_stop", 1, &start_and_stop_cb);
	//ros::Subscriber manual_auto=n.subscribe<std_msgs::Float64>("/manual_or_automatic", 1, manual_or_automatic_cb); //aggiunta riga per impostare controllo manuale o automatico

	// MOD Luca @ 13-08-2020 commented line 
	// Scommentato da FEDE il publisher sottostante
	ros::Publisher heading_angle= n.advertise<geometry_msgs::Point>("/orientation",100); 
	serial_init();

	/// INIZIALIZZAZIONE
    	// front/back position
	pos_x_f = 0;
	pos_y_f = 0;
	pos_z_f = 0; 

	pos_x_b = 0;
	pos_y_b = 0;
	pos_z_b = 0;

	// start and stop
	startstop = 0;

	// waypoint to reach
	way_x = 0;
	way_y = 0;
	way_z = 0;

	// robot current pose
	robot_pose_x = 0;
	robot_pose_y = 0;
	robot_pose_z = 0;

	// inizializza rx
	new_message_available = false;

  	ros::Rate loop_rate(100); //100


	while (ros::ok())
	{
		//unsigned char msg[] = { 'H', 'e', 'l', 'l', 'o', '\n \r' };
		//write(serial_port, msg, sizeof(msg));	
		read_from_serial();
		if (new_message_available)
		{
			h_angle.z=heading;
          	heading_angle.publish(h_angle);
	    	new_message_available = false;
		}
	    	



		// ----------------------------------

		unsigned char a[10];
		a[0] = (unsigned char) 26;
		write(serial_port, a, 1);

		a[0] = (unsigned char) 27;
		write(serial_port, a, 1);

		a[0] = (unsigned char) 44;
		write(serial_port, a, 1);


		// ----------------------------------

		d.n = (float) pos_x_f;
		write(serial_port, (const void*) d.s, 4);

		d.n = (float) pos_y_f;
		write(serial_port, (const void*) d.s, 4);

		d.n = (float) pos_z_f;
		write(serial_port, (const void*) d.s, 4);

			// ---------------------------------

		d.n = (float) pos_x_b;
		write(serial_port, (const void*) d.s, 4);	

		d.n = (float) pos_y_b;
		write(serial_port, (const void*) d.s, 4);

		d.n = (float) pos_z_b;
		write(serial_port, (const void*) d.s, 4);
	
		// ----------------------------------

		d.n = (float) way_x;
		write(serial_port, (const void*) d.s, 4);	

		d.n = (float) way_y;
		write(serial_port, (const void*) d.s, 4);

		d.n = (float) way_z;
		write(serial_port, (const void*) d.s, 4);

		// ----------------------------------

		d.n = (float) startstop;
		write(serial_port, (const void*) d.s, 4);

		// ----------------------------------

		d.n = (float) robot_pose_x;
		write(serial_port, (const void*) d.s, 4);	


		d.n = (float) robot_pose_y;
		write(serial_port, (const void*) d.s, 4);


		d.n = (float) robot_pose_z;
		write(serial_port, (const void*) d.s, 4);

		ros::spinOnce();
		loop_rate.sleep();

	//sleep(1);
	}
	
}

int serial_init()
{
	serial_port = open("/dev/ttyUSB1", O_RDWR);

	// Check for errors
	if (serial_port < 0) 
	{
	    printf("Error %i from open: %s\n", errno, strerror(errno));
	}
	else
	{
		printf("port %s correctly opened \n", "/dev/ttyUSB1");	
	}
	// Create new termios struc, we call it 'tty' for convention
	// No need for "= {0}" at the end as we'll immediately write the existing
	// config to this struct
	struct termios tty;

	// Read in existing settings, and handle any error
	if(tcgetattr(serial_port, &tty) != 0) 
	{
		printf("Error %i from tcgetattr: %s\n", errno, strerror(errno));
	}
	else
	{
		printf("configuring serial port ... \n");			
	}

	tty.c_cflag &= ~PARENB; // Clear parity bit, disabling parity (most common)
	// tty.c_cflag |= PARENB;  // Set parity bit, enabling parity

	tty.c_cflag &= ~CSTOPB; // Clear stop field, only one stop bit used in communication (most common)
	// tty.c_cflag |= CSTOPB;  // Set stop field, two stop bits used in communication

	// tty.c_cflag |= CS5; // 5 bits per byte
	// tty.c_cflag |= CS6; // 6 bits per byte
	// tty.c_cflag |= CS7; // 7 bits per byte
	tty.c_cflag |= CS8; // 8 bits per byte (most common)

	tty.c_cflag &= ~CRTSCTS; // Disable RTS/CTS hardware flow control (most common)
	// tty.c_cflag |= CRTSCTS;  // Enable RTS/CTS hardware flow control

	tty.c_cflag |= CREAD | CLOCAL; // Turn on READ & ignore ctrl lines (CLOCAL = 1)

	tty.c_lflag &= ~ICANON;	// disable canoical mode

	tty.c_lflag &= ~ECHO; // Disable echo
	tty.c_lflag &= ~ECHOE; // Disable erasure
	tty.c_lflag &= ~ECHONL; // Disable new-line echo

	tty.c_lflag &= ~ISIG; // Disable interpretation of INTR, QUIT and SUSP

	tty.c_iflag &= ~(IXON | IXOFF | IXANY); // Turn off s/w flow ctrl

	tty.c_iflag &= ~(IGNBRK|BRKINT|PARMRK|ISTRIP|INLCR|IGNCR|ICRNL); // Disable any special handling of received bytes

	tty.c_oflag &= ~OPOST; // Prevent special interpretation of output bytes (e.g. newline chars)
	tty.c_oflag &= ~ONLCR; // Prevent conversion of newline to carriage return/line feed
	// tty.c_oflag &= ~OXTABS; // Prevent conversion of tabs to spaces (NOT PRESENT IN LINUX)
	// tty.c_oflag &= ~ONOEOT; // Prevent removal of C-d chars (0x004) in output (NOT PRESENT IN LINUX)

	tty.c_cc[VTIME] = 10;    // Wait for up to 1s (10 deciseconds), returning as soon as any data is received.
	tty.c_cc[VMIN] = 0;


	///////////////
	// BAUD RATE //
	///////////////
	// Set in/out baud rate to be 9600
	// Ppossible BAUDs: B0,  B50,  B75,  B110,  B134,  B150,  B200, B300, B600, B1200, B1800, B2400, B4800, B9600, B19200, B38400, B57600, B115200, B230400, B460800
	cfsetispeed(&tty, B115200);
	cfsetospeed(&tty, B115200);

	// Specifying a custom baud rate when using GNU C
	//cfsetispeed(&tty, 104560);
	//cfsetospeed(&tty, 104560);

	// Save tty settings, also checking for error
	if (tcsetattr(serial_port, TCSANOW, &tty) != 0) 
	{
	    printf("Error %i from tcsetattr: %s\n", errno, strerror(errno));
	}
	else
	{
		printf("serial port configured \n");
	}



}


void Pose_cb_forward(const geometry_msgs::PoseStamped::ConstPtr& msg)
{
    pos_x_f = msg->pose.position.x;
    pos_y_f = msg->pose.position.y;
    pos_z_f = msg->pose.position.z;
  	ROS_INFO("Pose_cb_forward-> pos_x_f: %f pos_y_f: %f pos_z_f: %f \n",pos_x_f, pos_y_f, pos_z_f  );

}
void Pose_cb_back(const geometry_msgs::PoseStamped::ConstPtr& msg)
{
    pos_x_b = msg->pose.position.x;
    pos_y_b = msg->pose.position.y;
    pos_z_b = msg->pose.position.z;
  	ROS_INFO("Pose_fb_forward-> pos_x_b: %f pos_y_b: %f pos_z_b: %f \n",pos_x_b, pos_y_b, pos_z_b  );

}
void start_and_stop_cb(const std_msgs::Float64::ConstPtr& msg)
{
    startstop=double(msg->data);
      
}
void waypoint_cb(const geometry_msgs::Point::ConstPtr& msg)
{
     way_x = msg->x ;
     way_y = msg->y;
     way_z = msg->z;
}

void robot_pose_cb(const geometry_msgs::Point::ConstPtr& msg)
{
     robot_pose_x = msg->x;
     robot_pose_y = msg->y;
     robot_pose_z = msg->z;
}


////////////////////////////////////// RCV

////////////////////////LEGGI DA SERIALE////////////////////



void parser_mess(unsigned char buffer){
	static state state_msg = HEADER_1;


        //DEBUG 
        ROS_INFO("parser");
        //ROS_INFO_STREAM("Init  parser_mess ( called by read_from_serial "  );
        //ROS_INFO_STREAM("[parser_mess] new_packet:  " << new_packet  );
        // ROS_INFO_STREAM("Char arrived:  " << std::hex <<  buffer   );
        //ROS_INFO_STREAM("Char arrived:  " << std::dec <<  buffer   );

    //implementazione della macchina a stati
    switch(state_msg){
        case HEADER_1:

            if(buffer == HEADER_A)
            {
                state_msg=HEADER_2;
            }else
            {
                state_msg=HEADER_1;
            }
            break;

        case HEADER_2:
            if(buffer == HEADER_B)
            {
                state_msg=ID;
                //è stato riconosciuto un header-->è in arrivo un nuovo pacchetto
                
            }
            else
            {
                state_msg=HEADER_1;
            }
            break;

        case ID:
            //if(buffer == PAYLOAD_POSE_R)
            if(buffer == PAYLOAD_POSE)
            {
                state_msg=wait_PAYLOAD;
                //è stato riconosciuto un ID-->è in arrivo un nuovo pacchetto
                //ma non è ancora stato ricevuto e decodificato tutto
            }
            else
            {
                state_msg=HEADER_1;
            }
            break;




            /*********************************************************/
            //PACCHETTO CONTENTENTE POSIZIONI E ORIENTAZIONI
      case wait_PAYLOAD:
      	static int offset = 0;
            if(offset<4)
                {
                	
                    ROS_INFO(" WAIT PAYLOAD");
                   
                    //coda_recv_seriale.push(buffer);
                    rx_buf[offset] = buffer;
                    state_msg=wait_PAYLOAD;
                    offset++;
                    //ROS_INFO_STREAM("[parser_mess] offset:  " << offset  );   
                    
                }
            if(offset==4)
               {   
                                    ROS_INFO(" offset 1");
           //ROS_INFO_STREAM("Arrived six numbers encoded ( and new_packet incremented  "  );   
         
                    offset=0;
                    state_msg=HEADER_1;
                    //cout << "ricevuto payload " << endl;
                    //ROS_INFO_STREAM("[parser_mess] Good: we have received  payload "  );   
                    //ROS_INFO_STREAM("[parser_mess] new_packet:  " << new_packet  );   
                    // return msg;
                    decode_payload();
                }

            break;
    }

    return;
}


void decode_payload()
{
    union D{
       char   s[4];
       float  n;
       } d;
           
    //in coda_recv_seriale ho 4 bytes da decodificare
    d.s[0] = rx_buf[0];
    d.s[1] = rx_buf[1];
    d.s[2] = rx_buf[2];
    d.s[3] = rx_buf[3];
  
    
    heading = (double) d.n;
    new_message_available = true;
}


/*****************************************************************/
/*                                                               */
/*                 READ SERIALE                                  */
/*****************************************************************/
void read_from_serial()
{
    int bytes = 0;

    unsigned char buf[1024];

    //DEBUG 

    // Read data from the COM-port
    bytes = read(serial_port, buf, sizeof buf);

    for(int a = 0 ; a < bytes ; a++)
    {
    	ROS_INFO("dato ricevuto");
        parser_mess(buf[a]); 
    }

 }    
      
