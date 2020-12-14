/* software watchdog example */

#include <stdio.h>
#include <unistd.h>
#include <sys/stat.h>
#include <sys/types.h>
#include <sys/fcntl.h>
#include <sys/ioctl.h>
#include <stdlib.h>
#include <errno.h>
#include <syslog.h>
#include <signal.h>
#include <stdbool.h>
#include <sys/wait.h>


int forkIndependentProc(char *prog, char **arg_list)
{
	pid_t child;

	if ((child = fork()) < 0) {
		/* parent: check if fork failed */
		//PR_ERR("fork error");
	} else if (child == 0) {
		/* 1st level child: fork again */
		if ((child = fork()) < 0) {
			//PR_ERR("fork error");
		} else if (child > 0) {
			/* 1st level child: terminate itself to make init process the parent of 2nd level child */
			exit(0);
		} else {
			/* 2nd level child: execute program and will become child of init once 1st level child exits */
			execvp(prog, arg_list);
			//PR_ERR("execvp error");
			exit(0);
		}
	}

	/* parent: wait for 1st level child ends */
	waitpid(child, NULL, 0);

	return child;
}

bool checkApp(const char *app_name)
{
	FILE *fp;
	char buffer[128];
	bool ret = true;
	//Detect swann_service status
	char cmd[128] = {};
	sprintf(cmd, "ps | grep -v \"grep\" | grep \"%s\"", app_name);

	fp = popen(cmd, "r");
	if (fp == NULL) {
		syslog(LOG_INFO, "%s: Failed to run command\n", app_name);
		exit(1);
	}

	if (fgets(buffer, sizeof(buffer) - 1, fp) == NULL) {
		//setLEDInform("Critical_Error", 1);
		syslog(LOG_INFO, "Failed to find %s\n", app_name);
		char *app_argv[] = { "chrt", "-r", "50", "<another_app>", "1", "-n", NULL };
		forkIndependentProc("/usr/bin/chrt", app_argv);
		ret = false;
	} else {
		//syslog(LOG_INFO, "app: %s", buffer);
	}

	pclose(fp);

	return ret;
}

int main(int argc, char **argv)
{
	bool app_ret;
	int count = 0;
	char *app_name = argv[1];

	while (1) {
		app_ret = true;
		app_ret = checkApp(app_name);

		if (access("/tmp/app2_ready", F_OK) == 0) {
			app_ret = checkApp();
		}

		if (!app_ret) {
			/* kill watchd and reboot system */
			sleep(270);
			system("killall -2 watchd");
			break;
		}

		if (count >= 3) {
			sleep(240);
			system("killall -2 watchd");
			break;
		}

		sleep(10);
	}

	return 0;
}
