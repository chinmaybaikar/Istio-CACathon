#!/usr/bin/python

import os
import itertools
import threading
import time
import sys



def konfig():
    # Setting up alias and kubeconfig to use later during install
    config = input("\nPlease provide the path to your kubeconfig: ")
    kubeconfig = str(config)
    #subprocess.call("alias kc='kubectl --kubeconfig=$kubeconfig'",shell=True)
    os.system("alias kc='kubectl --kubeconfig=$kubeconfig'")
    print('Setting the kubeconfig...')
    return kubeconfig

def install():
    kubeconfig=konfig()
    # Downloading Istio v1.11.4 and setting up the env
    done = False
    def animate():
        for c in itertools.cycle(['|', '/', '-', '\\']):
            if done:
                break
            sys.stdout.write('\rloading ' + c)
            sys.stdout.flush()
            time.sleep(0.1)
        sys.stdout.write('\rDownloaded Istio v1.11.4!\n\n')

    t = threading.Thread(target=animate)
    t.start()

    download_script = 'curl -sL https://istio.io/downloadIstio | ISTIO_VERSION=1.11.4 sh - > /dev/null'
    os.system(download_script)
    time.sleep(5)
    done = True

    # Installing istioctl
    install_istioctl = 'cd istio-1.11.4; export PATH=$PWD/bin:$PATH; istioctl -c {} install'
    os.system(install_istioctl .format(kubeconfig))

    # Adding a custom label to the default namespace
    sys.stdout.write('\n************* Adding custom labels to default namespace *************\n')
    label_namespace = 'kubectl --kubeconfig={} label namespace default istio-injection=enabled'
    os.system(label_namespace .format(kubeconfig))

    # Install Demo application
    sys.stdout.write('\n************* Installing demo application *************\n')
    install_app = 'kubectl --kubeconfig={} apply -f https://raw.githubusercontent.com/GoogleCloudPlatform/microservices-demo/master/release/kubernetes-manifests.yaml'
    os.system(install_app .format(kubeconfig))

    # Installing telemetry and visualization tools
    sys.stdout.write('\n************* Installing telemetry and visualization tools *************\n')
    install_addons = 'kubectl --kubeconfig={} apply -f ./istio-1.11.4/samples/addons'
    os.system(install_addons .format(kubeconfig))

    # Initiating port forwarding to access Kiali dashboard
    sys.stdout.write('\n************* Initiating port forwarding to access Kiali dashboard *************\n')
    print ("\nProceed to use 127.0.0.1:20001 in your web browser to access the Kiali dashboard\n")
    install_addons = 'kubectl --kubeconfig={} port-forward service/kiali -n istio-system 20001'
    os.system(install_addons .format(kubeconfig))
    

def uninstall():
    kubeconfig=konfig()
    # Removing istioctl
    uninstall_istioctl = 'kubectl --kubeconfig={} delete namespace istio-system'
    os.system(uninstall_istioctl .format(kubeconfig))
    print ("Deleted istio-system namespace\n")

    # Removing istioctl
    remove_label_ns = 'kubectl --kubeconfig={} label namespace default istio-injection-'
    os.system(remove_label_ns .format(kubeconfig))
    print ("Deleted custom labels from default namespace\n")
    
    # Removing Demo application and add-ons
    uninstall_app = 'kubectl --kubeconfig={} delete -f https://raw.githubusercontent.com/GoogleCloudPlatform/microservices-demo/master/release/kubernetes-manifests.yaml'
    os.system(uninstall_app .format(kubeconfig))
    uninstall_addons = 'kubectl --kubeconfig={} delete -f ./istio-1.11.4/samples/addons'
    os.system(uninstall_addons .format(kubeconfig))
    sys.stdout.write('\nCleanup completed successfully\n')
    


while True:
    try:
        option = str(input("\nThis is a utility to install or remove Istio and a demo application for testing\n" +
                       "\n1) Install Istio and the demo application\n" +
                       "2) Remove the demo application along with Istio and its addons\n" +
                       "\nPlease select from the above options: "))
        
        if option == "1":
            install()
            break
            
        elif option == "2":
            uninstall()
            break
            
        else:
            print("\nPlease input one of the options")
        
    except:
        break