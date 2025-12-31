# Command Line Aliases Generator

Boost your productivity with these essential Kubernetes and cloud-native command line aliases for certification exams and daily operations.

## 🚀 Quick Setup

### Bash/Zsh Setup
```bash
# Add to ~/.bashrc or ~/.zshrc
source ~/k8s-aliases.sh
```

### Fish Shell Setup
```bash
# Add to ~/.config/fish/config.fish
source ~/k8s-aliases.fish
```

## 📋 Essential Kubernetes Aliases

### Basic kubectl Aliases
```bash
# Core commands
alias k=kubectl
alias kgp='kubectl get pods'
alias kgs='kubectl get services'
alias kgd='kubectl get deployments'
alias kgns='kubectl get namespaces'
alias kga='kubectl get all'

# Describe commands
alias kdp='kubectl describe pod'
alias kds='kubectl describe service'
alias kdd='kubectl describe deployment'
alias kdns='kubectl describe namespace'

# Delete commands
alias kdp='kubectl delete pod'
alias kds='kubectl delete service'
alias kdd='kubectl delete deployment'
alias kdns='kubectl delete namespace'

# Apply and create
alias kaf='kubectl apply -f'
alias kf='kubectl create -f'

# Logs
alias kl='kubectl logs'
alias klf='kubectl logs -f'

# Exec
alias ke='kubectl exec'
alias keit='kubectl exec -it'

# Config
alias kcn='kubectl config current-context'
alias kcg='kubectl config get-contexts'
alias kcuc='kubectl config use-context'
alias kcgns='kubectl config set-context --current --namespace'

# Namespace shortcuts
alias kga='kubectl get all --all-namespaces'
alias kgn='kubectl get nodes'
alias kgpv='kubectl get pv'
alias kpvc='kubectl get pvc'
```

### Advanced kubectl Aliases
```bash
# Watch commands
alias wkg='watch kubectl get'
alias wkgp='watch kubectl get pods'
alias wkgs='watch kubectl get services'

# Port forwarding
alias kpf='kubectl port-forward'

# Scale commands
alias ksc='kubectl scale deployment'

# Rollout commands
alias kru='kubectl rollout undo deployment'
alias krs='kubectl rollout status deployment'
alias krr='kubectl rollout restart deployment'

# Top commands
alias ktn='kubectl top nodes'
alias ktp='kubectl top pods'

# CP commands
alias kcp='kubectl cp'

# Label and annotate
alias kla='kubectl label'
alias kan='kubectl annotate'

# Get with wide output
alias kgpw='kubectl get pods -o wide'
alias kgsw='kubectl get services -o wide'
alias kdnw='kubectl get nodes -o wide'

# YAML output
alias kgy='kubectl get -o yaml'
 kdy='kubectl describe -o yaml'
```

## 🔧 Helm Aliases
```bash
# Basic Helm commands
alias h='helm'
alias hl='helm list'
alias hi='helm install'
alias hu='helm uninstall'
alias hg='helm get'
alias hh='helm history'
alias hr='helm rollback'
alias hs='helm search'
alias hsh='helm show'
alias hv='helm version'
alias hrepo='helm repo'
alias htpl='helm template'
alias hlint='helm lint'
alias hpkg='helm package'

# Helm repositories
alias hru='helm repo update'
alias hrl='helm repo list'
alias hra='helm repo add'
alias hrr='helm repo remove'

# Helm values
alias hval='helm show values'
alias hvals='helm get values'
```

## 🐳 Docker Aliases
```bash
# Basic Docker commands
alias d='docker'
alias di='docker images'
alias dps='docker ps'
alias dpsa='docker ps -a'
alias drun='docker run'
alias dstop='docker stop'
alias dstart='docker start'
alias dr='docker restart'
alias drm='docker rm'
alias drmi='docker rmi'
alias db='docker build'
alias dpull='docker pull'
alias dpush='docker push'
alias dexec='docker exec'
alias dlogs='docker logs'
alias dvol='docker volume'
alias dnet='docker network'

# Docker compose
alias dc='docker-compose'
alias dcup='docker-compose up'
alias dcdown='docker-compose down'
alias dcps='docker-compose ps'
alias dclogs='docker-compose logs'
alias dcb='docker-compose build'

# Docker system
alias dsys='docker system'
alias dsysp='docker system prune'
alias ddf='docker system df'
```

## ☸️ Minikube Aliases
```bash
# Minikube commands
alias mk='minikube'
alias mkstart='minikube start'
alias mkstop='minikube stop'
alias mkstatus='minikube status'
alias mkdelete='minikube delete'
alias mkip='minikube ip'
alias mkdashboard='minikube dashboard'
alias mkaddons='minikube addons'
alias mklogs='minikube logs'
alias mkprofile='minikube profile'
alias mknode='minikube node'
```

## 🔍 Istio Aliases
```bash
# Istio commands
alias i='istioctl'
alias ip='istioctl proxy-config'
alias ipil='istioctl proxy-config listeners'
alias ipir='istioctl proxy-config routes'
alias ipic='istioctl proxy-config clusters'
alias ipe='istioctl proxy-config endpoints'
alias ig='istioctl get'
alias id='istioctl describe'
alias il='istioctl logs'
alias iv='istioctl version'
alias iana='istioctl analyze'
alias iav='istioctl verify-install'
alias im='istioctl manifest'
```

## 📦 Package Manager Aliases
```bash
# APT (Debian/Ubuntu)
alias aptu='sudo apt update'
alias aptug='sudo apt upgrade'
alias apti='sudo apt install'
alias aptr='sudo apt remove'
alias apts='apt search'
alias aptsh='apt show'

# YUM/DNF (RHEL/CentOS/Fedora)
alias yumu='sudo yum update'
alias yumi='sudo yum install'
alias yumr='sudo yum remove'
alias yums='yum search'
alias yumsh='yum info'

# Homebrew (macOS)
alias brewu='brew update'
alias brewug='brew upgrade'
alias brewi='brew install'
alias brewr='brew uninstall'
alias brews='brew search'
alias brewsh='brew info'
```

## 🌐 Network Aliases
```bash
# Network utilities
alias ping='ping -c 4'
alias j='jobs'
alias ports='netstat -tuln'
alias myip='curl ifconfig.me'
alias myip6='curl ifconfig.co'
alias portsopen='ss -tuln'
alias netstat='netstat -tuln'

# SSH shortcuts
alias sshkey='ssh-keygen -t rsa -b 4096'
alias sshcopy='ssh-copy-id'
```

## 📁 File System Aliases
```bash
# Navigation
alias ll='ls -alF'
alias la='ls -A'
alias l='ls -CF'
alias ..='cd ..'
alias ...='cd ../..'
alias ....='cd ../../..'
alias home='cd ~'

# File operations
alias cp='cp -iv'
alias mv='mv -iv'
alias rm='rm -iv'
alias mkdir='mkdir -pv'
alias grep='grep --color=auto'
alias fgrep='fgrep --color=auto'
alias egrep='egrep --color=auto'

# Disk usage
alias du='du -h'
alias df='df -h'
alias dus='du -sh *'
```

## 🔍 Git Aliases
```bash
# Basic Git
alias g='git'
alias gs='git status'
alias ga='git add'
alias gc='git commit'
alias gp='git push'
alias gl='git pull'
alias gco='git checkout'
alias gb='git branch'
alias gd='git diff'
alias glg='git log --oneline'
alias gcl='git clone'
alias gsh='git stash'
alias gsp='git stash pop'

# Advanced Git
alias gcm='git commit -m'
alias gca='git commit --amend'
alias gcaa='git commit -a --amend'
alias gcp='git cherry-pick'
alias gr='git rebase'
alias grc='git rebase --continue'
alias gra='git rebase --abort'
alias gm='git merge'
alias gmt='git mergetool'
```

## 🎯 Certification Exam Specific Aliases

### CKA Exam Aliases
```bash
# CKA specific shortcuts
alias kcc='kubectl config current-context'
alias kcuc='kubectl config use-context'
alias kcns='kubectl config set-context --current --namespace'
alias kge='kubectl get events --sort-by=.metadata.creationTimestamp'
alias kgea='kubectl get events --all-namespaces --sort-by=.metadata.creationTimestamp'
alias krun='kubectl run'
alias kex='kubectl expose'
alias ksc='kubectl scale'
alias krs='kubectl rollout status'
alias krr='kubectl rollout restart'
alias kru='kubectl rollout undo'
```

### CKAD Exam Aliases
```bash
# CKAD specific shortcuts
alias kaf='kubectl apply -f'
alias kdf='kubectl delete -f'
alias kcf='kubectl create -f'
alias kdry='kubectl apply --dry-run=client -f'
alias kedit='kubectl edit'
alias kcp='kubectl cp'
alias katt='kubectl attach'
alias kport='kubectl port-forward'
alias kproxy='kubectl proxy'
alias kauth='kubectl auth can-i'
```

### CKS Exam Aliases
```bash
# CKS specific shortcuts
alias kpol='kubectl get policies'
alias kpsp='kubectl get podsecuritypolicies'
alias knet='kubectl get networkpolicies'
alias krole='kubectl get roles'
alias krb='kubectl get rolebindings'
alias kcr='kubectl get clusterroles'
alias kcrb='kubectl get clusterrolebindings'
alias ksa='kubectl get serviceaccounts'
alias ksec='kubectl get secrets'
```

## 📝 Custom Alias Generator

### Create Your Own Aliases
```bash
# Function to create custom aliases
create_alias() {
    local command=$1
    local alias_name=$2
    echo "alias $alias_name='$command'" >> ~/.bashrc
    source ~/.bashrc
    echo "Alias '$alias_name' created for '$command'"
}

# Example usage:
# create_alias "kubectl get pods --all-namespaces" "kga"
```

### Interactive Alias Creator
```bash
# Interactive alias creation function
add_alias() {
    echo "Enter the full command:"
    read full_command
    echo "Enter the alias name:"
    read alias_name
    echo "alias $alias_name='$full_command'" >> ~/.bashrc
    source ~/.bashrc
    echo "Alias '$alias_name' added successfully!"
}
```

## 🛠️ Installation Scripts

### Automatic Setup Script
```bash
#!/bin/bash
# setup-k8s-aliases.sh

echo "Setting up Kubernetes aliases..."

# Backup existing .bashrc
cp ~/.bashrc ~/.bashrc.backup

# Add aliases to .bashrc
cat >> ~/.bashrc << 'EOF'

# Kubernetes Aliases
source ~/k8s-aliases.sh

# Custom aliases
alias k=kubectl
alias kgp='kubectl get pods'
alias kgs='kubectl get services'
alias kga='kubectl get all --all-namespaces'
alias kdp='kubectl describe pod'
alias kds='kubectl describe service'
alias kaf='kubectl apply -f'
alias kl='kubectl logs'
alias keit='kubectl exec -it'
alias kcn='kubectl config current-context'
alias kcg='kubectl config get-contexts'
alias kcuc='kubectl config use-context'
alias kcgns='kubectl config set-context --current --namespace'

EOF

echo "Aliases added to ~/.bashrc"
echo "Run 'source ~/.bashrc' to activate aliases"
```

### Fish Shell Setup Script
```bash
#!/bin/fish
# setup-k8s-aliases.fish

echo "Setting up Kubernetes aliases for Fish..."

# Create aliases file
cat > ~/.config/fish/k8s-aliases.fish << 'EOF'

# Kubernetes Aliases
alias k kubectl
alias kgp "kubectl get pods"
alias kgs "kubectl get services"
alias kga "kubectl get all --all-namespaces"
alias kdp "kubectl describe pod"
alias kds "kubectl describe service"
alias kaf "kubectl apply -f"
alias kl "kubectl logs"
alias keit "kubectl exec -it"
alias kcn "kubectl config current-context"
alias kcg "kubectl config get-contexts"
alias kcuc "kubectl config use-context"
alias kcgns "kubectl config set-context --current --namespace"

EOF

# Add to config.fish
echo 'source ~/.config/fish/k8s-aliases.fish' >> ~/.config/fish/config.fish

echo "Aliases added to Fish config"
echo "Restart Fish or run 'source ~/.config/fish/config.fish' to activate"
```

## 📚 Best Practices

### Alias Naming Conventions
1. **Use short, memorable names**
2. **Group related aliases**
3. **Avoid conflicts with existing commands**
4. **Use consistent patterns**

### Organization Tips
1. **Categorize aliases by tool**
2. **Add comments for complex aliases**
3. **Keep a backup of your aliases**
4. **Share with your team**

### Security Considerations
1. **Avoid aliases that hide dangerous commands**
2. **Be careful with rm aliases**
3. **Test aliases before adding to production**
4. **Document custom aliases**

## 🔗 Additional Resources

### Documentation
- [Kubectl Cheat Sheet](https://kubernetes.io/docs/reference/kubectl/cheatsheet/)
- [Helm Cheat Sheet](https://helm.sh/docs/intro/using_helm/)
- [Docker Cheat Sheet](https://docs.docker.com/get-started/docker_cheatsheet/)

### Community Resources
- [Awesome Kubernetes](https://github.com/ramitsurana/awesome-kubernetes)
- [Kubernetes Tools](https://kubernetes.io/docs/tasks/tools/)
- [Shell Customization](https://www.gnu.org/software/bash/manual/)

---

*Last Updated: December 2025*
*Compatible with Kubernetes 1.28+*
